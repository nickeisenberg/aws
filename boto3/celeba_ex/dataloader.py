from torchdata.datapipes.iter import IterableWrapper, S3FileLoader

dp_s3_urls = IterableWrapper(["s3://celeba-for-tut/imgs/",]).list_files_by_s3()
# In order to make sure data are shuffled and sharded in the
# distributed environment, `shuffle`  and `sharding_filter`
# are required. For detail, please check our tutorial in:
# https://pytorch.org/data/main/tutorial.html#working-with-dataloader
sharded_s3_urls = dp_s3_urls.shuffle().sharding_filter()


dp_s3_files = S3FileLoader(sharded_s3_urls)
for url, fd in dp_s3_files: # Start loading data
    data = fd.read()

# Functional API
dp_s3_files = sharded_s3_urls.load_files_by_s3(buffer_size=256)
for url, fd in dp_s3_files:
    data = fd.read()
