## re:Inforce 2024 DAP341 supporting code

This repository hosts sample code that supports the re:Inforce 2024 Code Talk with session ID DAP341.
The code in this repository is intentionally simple to optimize for readability during the session, and is not intended for use in a production setting.

The objective of the code in this repository is to demonstrate the functional core of a Retrieval Augmented Generation (RAG) chatbot, while highlighting some of the data protection considerations relevant for Generative AI workloads in general.

If you would like to deploy a RAG chatbot style use case with AWS in production, consider one of the following options:
- [Amazon Q Business](https://aws.amazon.com/q/business/)
- [Knowledge Bases for Amazon Bedrock](https://aws.amazon.com/bedrock/knowledge-bases/)
- [Generative AI Application Builder on AWS](https://aws.amazon.com/solutions/implementations/generative-ai-application-builder-on-aws/)

## Deployment Guide

This repository contains a series of Python "scripts" that can be executed to demonstrate a series of ideas.
The scripts are numbered because, when executed sequentially, they tell a story about how a RAG chatbot works, and how data can be protected within a GenAI-based workload.
However, the scripts are all standalone and idempotent and do not need to be run sequentially.  

Some of the Python scripts provided here need to be modified before they run.
The scripts are stored here exactly as they are shown in the re:Inforce presentation for consistency.
Instances where you must update the script are annotated with `#UPDATE_TO_RUN_YOURSELF`.

The AWS resources required to run the Python example scripts, e.g. an Amazon Kendra index, example data, etc., *can* be provided by the user of this repository, but below are instructions for how these resources *could* be created.

### Prerequisites

- AWS account
- AWS user/role with sufficient permissions to deploy the CloudFormation template and run the Python code.
- AWS credentials configured per [instructions for boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/configuration.html)
- Python 3
- boto3 Python library installed

### Step-by-step guide

The main AWS resources that need to be created and referenced before the Python scripts will work are an Amazon Kendra Index and an accompanying Kendra Data Source that points to data on an Amazon S3 bucket.
Note that an Amazon Kendra Index has a non-negligible cost, and care should be taken to understand those [costs](https://aws.amazon.com/kendra/pricing/) before you deploy this solution.  

The code provided in this repository is intended to be complementary to a deployment of the Generative AI Application Builder on AWS.  If you deploy the Generative AI Application Builder on AWS, and proceed to deploy a "text" use case deployment with the "RAG" option enabled, a Kendra Index can be created for you as shown in the following section:

#### Generative AI Application Builder deployment

Deploy the Generative AI Application Builder on AWS Solution per the [deployment guide](https://docs.aws.amazon.com/solutions/latest/generative-ai-application-builder-on-aws/deploy-the-solution.html).  

As it relates to data protection, consider deploying the solution with the VPC option enabled, which minimizes traffic flowing over the public internet by leveraging VPC endpoints.

After the Deployment Dashboard is deployed, you will be able to [Deploy a use case](https://docs.aws.amazon.com/solutions/latest/generative-ai-application-builder-on-aws/step-2-deploy-use-case.html).  

When deploying a Use Case, select the `text` option.  In the `Select knowledge base` section, select `yes` to the RAG option, choose `Kendra` as the knowledge base, and, if you do not already have a Kendra Index, select `no` to "Do you have an existing Kendra index?" to have one created for you.
All other default values are fine, but adjust if/as needed to suit your needs.

#### Add Kendra Data Source

Once your Generative AI Application Builder is deployed, you will have an Amazon Kendra Index.
You now need to add a Kendra Data Source to that Index.
First, create or re-use an existing Amazon S3 bucket to store out data.
Upload the contents of the `data` directory, as well as the `src/kendra-acl.json` in this repository to that S3 bucket such that the resulting structure looks like this:
```
engineering/rootrunner3k-techspecs.txt
wiki/ecorobopotato.txt
kendra-acl.json
```

Navigate to your Amazon Kendra Index in the AWS Management Console, and choose the `Add Data Sources` option. 
Choose the `Amazon S3 connector` option.
Give the data source a name.
Create an IAM role, or use an existing one as desired.
In `Configure sync settings`, enter the location of your S3 bucket, set the `kendra-acl.json` file in the `Access control list configuration file location` setting, expand `Additional configuration`, and add `engineering` and `marketing` as prefixes to be indexed.
All other default values are sufficient to create and deploy your Kendra Data Source.
Once the Data Source is created, you must initiate a Data Source `sync` operation at least once, and wait for that sync to complete before running any Python scripts.

#### Enable Amazon Bedrock models

Before you can call any Amazon Bedrock models, you must enable [model access](https://docs.aws.amazon.com/bedrock/latest/userguide/model-access.html).  This repository uses Claude 3 Sonnet, so at least this model must be enabled.

#### CloudWatch Model invocation logging

In order to run the CloudWatch python file specifically, you must enable Amazon Bedrock model invocation logging, specifically with an [Amazon CloudWatch Logs destination](https://docs.aws.amazon.com/bedrock/latest/userguide/model-invocation-logging.html#setup-cloudwatch-logs-destination).  
As part of this process, you will create a CloudWatch Logs group, which must be updated in the accompanying Python script.

#### Create a Bedrock Guardrail

To run the Python scripts related to Bedrock Guardrails, you must create a Bedrock Guardrail.
To do so using the AWS Management Console, navigate to the Amazon Bedrock service and select the Guardrails section.  Choose `Create guardrail`.  Give it a name and set it up with defaults or whichever options you prefer.  However, ensure that in the `Add sensitive information filters` section, you add the `Address` PII type, and select `Mask` as the Guardrail behavior.  This ensures that your Guardrail will replicate the behavior that is intended to be demonstrated in the Python scripts in this project.

## Walkthrough

The markdown files, images, and python code file in the `src` directory are intended to be seen and executed in the order specified by their numbering scheme.  As follows is an explanation for each file to help guide the reader through the intention of the presentation that accompanies these code samples.

### 00_intro.md

Gives the main point of these code snippets, which is to show you very simplified Python code that is readable and demonstrates how RAG works at a basic level, while also highlighting data protection considerations for GenAI workloads more broadly.

### 01_ecorobopotato.png

Image used to introduce the notional product and organization whose data we are using.
The data is intentionally absurd so that LLMs will not accidentially have any training data related to this notional product or organization.  However, since this accompanying repository is now open source, it's possible that an LLM may eventually use this repository as a training data source, which may eventually break this assumption!

### 02_data.py

Simply shows the contents of the Amazon S3 bucket that we set up that contains our source data.  It also highlights the encryption type for this data on S3 to stress the importance of encrypting data at rest.

### 03_kendra.py

Prints out some of the basic information about our Amazon Kendra index to introduce the concept of Kendra and how it is able to perform semantic searches against our data sources.

### 04_kendra_retrieve.py

Demonstrates a simple `retrieve` API call against our Kendra index, which retrieves context based on the question we ask.

### 05_bedrock_standalone.py

Calls Amazon Bedrock and asks a question unrelated to our notional proprietary data.  This is intended to demonstrate how a LLM is able to answer many questions about things that are publicly available, because LLMS are often trained against massive amounts of data scraped from the open internet.

### 06_bedrock_proprietary_no_rag.py

Calls Bedrock and asks a question about our proprietary data.  Demonstrates how an LLM cannot answer questions about data that is proprietary and that has not been part of its training dataset.  

### 07_rag.py

First calls Kendra to retrieve relevant context from our proprietary data, and then uses that context when calling an LLM in Amazon Bedrock.  This pattern is called Retrieval Augmented Generation, or RAG.

### 08_rag_not_authorized.py

Adds in the Access Control List in the call to Amazon Kendra.  Because our "Marketing" group is not allowed to access the technical specifications document from kendra, our answer does not include details about content that Marketing is not authorized to view.  This demonstrates how we can achieve document-level authorization when using a RAG based approach.
It's worth noting that if you instead use your proprietary data to perform fine-tuning or continued pre-training to customize an LLM, you lose that ability to do fine-grained authorization at a document level; your users either have access to that customized model or they do not.

### 09_rag_address.py

Performs a RAG query that includes a specific address.  But perhaps we do not want addresses, or other types of PII or sensitive/harmful content to be included in our chatbot...

### 10_guardrail.py

Simply lists our some of the attributes of a precreated Amazon Bedrock Guardrail that we will use in the following step.  Specifically, we see that our Guardrail redacts Address data types.

### 11_rag_guardrail.py

Performs the same RAG-based call as 09_rag_address.py, but adds in the Bedrock Guardrail as part of the call to Bedrock.  This in turn redacts the specific address PII data from the response.

### 12_cloudtrail.py

Lists out 3 recent CloudTrail instances of invoking Bedrock.  This simply demonstrates how CloudTrail can b used to audit usage of the Amazon Bedrock service.  Other AWS services also generate CloudTrail events, and this data can be used to audit and protect your AWS resources.

### 13_cloudwatch.py

Lists out 3 recent CloudWatch model invocation logs.  This demonstrates how your data can be included in CloudWatch Model Invocation logs.  Therefore, if you enable model invocation logs, you must protect them with the same level of care that you protect the data source itself.

## Key Take-aways

After running the Python scripts, you will have been guided through some examples that demonstrate data protection considerations for Generative AI workloads.  Some of the key take-aways are:

* Data protection basics still apply.
    * Encryption @ rest + in transit
    * Least privilege permissions for apps + humans
    * Scan for sensitive data -> redact/remove appropriately
    * Audit changes to security resources

* Generative AI introduces some new considerations
    * Amazon Bedrock -> your prompt data is not used to train models
    * Amazon Bedrock -> we do not log your prompts/responses
    * Amazon Bedrock -> you can opt-in to model invocation logging. if you do, protect those logs
    * Amazon Bedrock -> use CloudTrail to audit usage, changes
    * Amazon Bedrock -> use VPC endpoints to avoid traversing public web
    * RAG -> document-level access control
    * Customized model -> no document-level access control
    * Amazon Bedrock Guardrails -> extra layer of protection to filter/block harmful, sensitive data
    * Chatbots -> chat history may contain sensitive data -> protect it

## Security

See [CONTRIBUTING](CONTRIBUTING.md#security-issue-notifications) for more information.

## License

This library is licensed under the MIT-0 License. See the LICENSE file.

