provider "aws" {
  region = "ap-south-1"
}

resource "aws_ecr_repository" "shama" {
  name = "shama_ch"
}

resource "null_resource" "docker_build_push" {

  provisioner "local-exec" {
    command = <<EOT
      aws ecr get-login-password --region ap-south-1 | \
      docker login --username AWS --password-stdin ${aws_ecr_repository.shama.repository_url}

      docker build -t my-image .
      docker tag my-image:latest ${aws_ecr_repository.shama.repository_url}:latest
      docker push ${aws_ecr_repository.shama.repository_url}:latest
    EOT
  }

  depends_on = [aws_ecr_repository.shama]
}

resource "aws_security_group" "sg" {
  name = "docker-sg"

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 8000
    to_port     = 8000
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_iam_role" "ec2_role" {
  name = "ec2-ecr-role-shama"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Principal = {
        Service = "ec2.amazonaws.com"
      }
    }]
  })
}

resource "aws_iam_role_policy_attachment" "ecr_policy" {
  role       = aws_iam_role.ec2_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryReadOnly"
}

resource "aws_iam_instance_profile" "profile" {
  name = "ec2-profile-shama"
  role = aws_iam_role.ec2_role.name
}

resource "aws_instance" "ec2" {
  ami           = "ami-05d2d839d4f73aafb"
  instance_type = "t3.micro"
  key_name      = "pk"

  security_groups      = [aws_security_group.sg.name]
  iam_instance_profile = aws_iam_instance_profile.profile.name

  #16GB storage (IMPORTANT)
  root_block_device {
    volume_size = 16
    volume_type = "gp2"
  }

  user_data = <<EOF
#!/bin/bash

# Log everything (VERY IMPORTANT for debugging)
exec > /var/log/user-data.log 2>&1

# Update system
apt-get update -y

# Install required packages
apt-get install -y unzip curl

apt-get install -y docker.io
systemctl start docker
systemctl enable docker

# Allow ubuntu user to use docker (optional but good)
usermod -aG docker ubuntu
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
./aws/install

# Verify AWS CLI
/usr/local/bin/aws --version

/usr/local/bin/aws ecr get-login-password --region ap-south-1 | \
docker login --username AWS --password-stdin ${aws_ecr_repository.shama.repository_url}

docker pull ${aws_ecr_repository.shama.repository_url}:latest

docker run -d -p 8000:8000 ${aws_ecr_repository.shama.repository_url}:latest

EOF

  depends_on = [null_resource.docker_build_push]

  tags = {
    Name = "Docker-ECR-EC2-Ubuntu"
  }
}