from io import BytesIO
import asyncio

from minio import Minio

class   Storage:
    def __init__(
        self,
        *,
        addr: str,
        access_key: str,
        secret_key: str,
        buckets: list,
        secure: bool = False,
    ):
        self.addr = addr
        self._base_buckets = buckets

        self._client = Minio(
            addr,
            access_key=access_key,
            secret_key=secret_key,
            secure=secure,
        )

        self.start()

    def start(self):
        for bucket in self._base_buckets:
            exists = self._client.bucket_exists(bucket)
            
            if not exists:
                self._client.make_bucket(bucket)

    async def upload_bytes(
        self,
        bucket: str,
        object_name: str,
        data: bytes,
        content_type: str = "application/octet-stream",
    ):
        stream = BytesIO(data)

        await asyncio.to_thread(
            self._client.put_object, bucket, object_name,
            stream, len(data), content_type
        )


    async def upload_png(
        self,
        bucket: str,
        object_name: str,
        data: bytes,
        content_type = "image/png"
    ):
        await self.upload_bytes(bucket, f"{object_name}.png", data, content_type)
        return {"bucket":bucket, "key":object_name}
        

    async def download_obj(
        self, bucket, object_name
    ):
        await asyncio.to_thread(
            self._client.get_object, bucket, object_name
        )