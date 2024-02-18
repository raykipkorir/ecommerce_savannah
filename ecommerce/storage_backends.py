from storages.backends.s3 import S3Storage


class StaticStorage(S3Storage):
    location = "static"
    # default_acl = "public-read"


class PublicMediaStorage(S3Storage):
    location = "media"
    # default_acl = "public-read"
    file_overwrite = "False"
