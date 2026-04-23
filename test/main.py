import asyncio
import logging

logging.basicConfig(level=logging.INFO)

async def handle_client(reader, writer):
    addr = writer.get_extra_info("peername")
    logging.info(f"[+] {addr}")

    try:
        while True:
            data = await reader.read(4096)
            if not data:
                break

            msg = data.decode(errors="ignore")
            logging.info(f"[{addr}] {msg}")

            writer.write(data)
            await writer.drain()

    except (ConnectionResetError, BrokenPipeError):
        logging.info(f"[-] {addr} disconnected abruptly")

    except Exception as e:
        logging.error(f"Error with {addr}: {e}")

    finally:
        try:
            writer.close()
            await writer.wait_closed()
        except Exception:
            pass

        logging.info(f"[-] {addr} closed")


async def main():
    server = await asyncio.start_server(handle_client, "0.0.0.0", 9000)

    logging.info("TCP listening on 9000")

    async with server:
        await server.serve_forever()

asyncio.run(main())