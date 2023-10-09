"""
SSH into the instance with 
ssh -i <keypair.pem> ubuntu@EC2PublicIpAddress

Remember to 
chmod 0400 keypair.pem
"""

import boto3
import json
import io
import pandas as pd
import torch
import numpy as np

with open("/home/ubuntu/GitRepos/OFFLINE/password.json") as oj:
    pw = json.load(oj)

ACCESS_KEY = pw['aws_ACCESS_KEY']
SECRET_ACCESS_KEY = pw['aws_SECRET_ACCESS_KEY']

session = boto3.Session(
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_ACCESS_KEY,
    # profile_name="",
    region_name="us-east-2"
)

# Create a s3 client that can make s3 buckets
s3_client = session.client('s3')

# create the resource 
s3_res = session.resource('s3')

buckets = [bucket['Name'] for bucket in s3_client.list_buckets()['Buckets']]
bucket_name = 'my-boto3-practice'

training_data = []
for i in [0, 1]:
    data = s3_client.get_object(
        Bucket='my-boto3-practice', 
        Key="clusters/" + f"cluster_{i}.csv"
    )['Body'].read().decode("utf-8")
    training_data.append(pd.read_csv(io.StringIO(data)))

training_data = pd.concat(training_data, axis=0)

class Model:
    
    def __init__(
        self, 
        W=torch.randn(size=(2,1), requires_grad=True), 
        b=torch.randn(size=(1,1), requires_grad=True), 
        lr=.01
    ):
        self.W = W
        self.b = b
        self.lr = lr

    def forward(self, input):
        return torch.nn.functional.sigmoid(torch.matmul(input, self.W) + self.b)
    
    @staticmethod
    def loss_fn(guesses, targets):
        return torch.mean((guesses - targets) ** 2)
    
    def train(
        self, 
        inputs, 
        targets,
        epochs=1
    ):

        running_loss = 0

        for epoch in range(1, epochs + 1):

            guesses = self.forward(inputs)
            loss = self.loss_fn(guesses, targets)

            running_loss += loss.item()

            if epoch % 10 == 0:
                print(f"LOSS: {running_loss / epoch}")

            loss.backward()
            
            with torch.no_grad():
                self.W -= self.W.grad * self.lr
                self.b -= self.b.grad * self.lr

                self.W.grad.zero_() 
                self.b.grad.zero_()

inputs = torch.tensor(
    training_data[['x', 'y']].values, dtype=torch.float32
)
labels = torch.tensor(
    training_data['labels'].values.reshape((-1, 1)), dtype=torch.float32
)

model = Model()

model.train(inputs, labels, epochs=5000)

guesses = model.forward(inputs)

np.where(
    (labels.detach().numpy() - np.round(guesses.detach().numpy())) != 0
)[0].size
