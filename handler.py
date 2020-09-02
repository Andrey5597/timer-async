import aiohttp
import asyncio
import time
import ast
import json


async def get_load_time(session, url):
    start_time = time.time()
    try:
        async with session.get(url) as response:
            await response.release()
            return {url: time.time()-start_time}
    except Exception:
        return {url: 'Invalid URL'}


async def main(event):
    async with aiohttp.ClientSession() as session:
        try:
            list_of_urls = ast.literal_eval(event.get('body'))
        except Exception:
            return {
                "statusCode": 400,
                "body": json.dumps(["Bad request data. There should be a list of urls in POST request body."])}
        coroutines = [get_load_time(session, url) for url in list_of_urls]
        results = await asyncio.gather(*coroutines, return_exceptions=True)
        return {"statusCode": 200, "body": json.dumps({k: v for d in results for k, v in d.items()}), "headers": {}}


def handler(event, context):
    return asyncio.run(main(event))
