import asyncio

loop = asyncio.get_event_loop()

async def main():
      await bot.start()
      await app.start()
      await call.start()
      await idle()

if __name__ == "__main__":
    loop.run_until_complete(main())