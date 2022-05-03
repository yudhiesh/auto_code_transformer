from modelstore import ModelStore

model_id = "029109097123412"

model_store = ModelStore.from_aws_s3(
    bucket_name="test_bucket",
    region="us-east-1",
    root_prefix="models",
)

model = model_store.load(
    domain="test_domain",
    model_id="1231238123891",
)

model2 = model_store.load(
    domain="test_domain",
    model_id=MODEL_ID,
)
