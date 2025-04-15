from starlette.requests import Request


async def get_client_ip(request: Request):
    client_ip = request.client.host  # 获取客户端的 IP 地址
    return client_ip
