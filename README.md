# Smart_Doctor
Smart Doctor is an AI tool with the capability to automatically answer medical questions submitted by users. To support this capability, an end-to-end infrastructure solution needs to be designed and implemented leveraging Llama-2 7B model and AWS services.

# Infrastructure for Smart Doctor Medical Question Answering

## Date

10-07-2023

## Context:

Smart Doctor needs to be able to automatically answer medical questions submitted by users. To support this capability, an end-to-end infrastructure solution needs to be designed and implemented leveraging MPT7B instruct model and AWS services.

## Status:

Implemented the infrastructure (Pre-Alpha release)

## Decision:

The infrastructure located in the EC2 instance inside a VPC will need to connect to the current MySQL database hosted in AWS RDS present in a different VPC in a different account. This is enabled through VPC peering between the 2 VPCs. The connection is established to retrieve new medical questions that have been submitted in the past 24 hours with the status as "new" or "answered". A scheduler Python script hosted on a free tier T2.micro EC2 instance will run indefinitely and every day, @ 12:00 a.m IST will trigger the smart doctor inference hosted in a large G5.2Xlarge instance to query the database and extract the question text and IDs. 

The raw question texts will then be cleansed and anonymized using OpenAI's moderation API to remove any personally identifiable information or irrelevant content. This preprocessed question text will be used as input to construct prompts for the machine-learning model.

Prompt construction will leverage vector similarity search on the existing database of questions/answers across all specializations to find the 5 most similar examples using similarity search. These example pairs will then be sorted in the ascending order of their total lengths and the 2 smallest example pairs will be formatted into zero-shot learning prompts with context to provide context and prime the model to generate high-quality responses.

The prompts and questions will be passed to the MPT-7B instruct model for inference with a maximum output length of 200 tokens and this will generate an answer text as output.

The generated answers will then be persisted back to the RDS MySQL database in a smart_doctor_answer table that links to the original question ID.

The cloud services required to implement this architecture include 2 EC2 instances (1 G5.2Xlarge, 1 T2.micro), RDS, VPC peering and Secrets Manager. 

Together this infrastructure provides a scalable, secure, and cost-effective platform to generate automated answers to medical questions submitted by users. The inference pipeline can be extended over time with new data and fine-tuning.

## Consequences:

- Requires setup and management of multiple cloud services
- Ongoing costs for cloud infrastructure (EC2 Instances, RDS)
- Engineering effort needed for testing, monitoring
- Retraining of model required as data changes over time

End-to-end infrastructure solution to retrieve query from RDS, generate their answers using MPT7B and persist the answers to the database has been implemented. 

