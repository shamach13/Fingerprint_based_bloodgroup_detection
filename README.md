Blood group identification is a critical component in medical diagnostics and transfusion processes. Traditionally, blood group detection requires invasive laboratory tests. 
With the increasing availability of biometric datasets and advancements in deep learning, this work explores an experimental, non-clinical approach to classify blood groups using fingerprint images. 
Using a publicly available fingerprint-based blood group dataset, a Convolutional Neural Network (CNN) is trained to learn visual patterns correlated with labeled blood group classes. 
The trained model is containerized using Docker to ensure reproducibility and portability, and a cloud-ready deployment architecture using AWS is proposed. 
This work is intended strictly for academic exploration and learning, not for medical diagnosis.

## Problem Statement
To design and evaluate a deep learning–based image classification system that predicts blood
group labels (A, B, AB, O) from fingerprint images using a publicly available dataset, and to
demonstrate containerized deployment readiness using Docker and AWS cloud
infrastructure.

## Objectives
 To study the feasibility of fingerprint image classification using deep learning.
 To train a CNN model for multi‑class blood group classification.
 To evaluate model performance using standard metrics such as accuracy and confusion
matrix.
 To containerize the trained model and inference API using Docker.
 To propose a cloud‑based deployment architecture using AWS for scalable access.
