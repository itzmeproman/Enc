from bot.fun.emojis import enmoji, enmoji2
from bot.fun.quips import enquip, enquip2
from bot.utils.log_utils import logger
from bot.workers.auto.status import autostat
from bot.workers.auto.transcode import something

from .before import *


async def start_aria2p():
    try:
        globals()["aria2"] = aria2p.API(
            aria2p.Client(host="http://localhost", port=ARIA2_PORT, secret="")
        )
        aria2.add(
            "https://nyaa.si/download/1690208.torrent",
            {"dir": f"{os.getcwd()}/downloads"},
        )
        await asyncio.sleep(2)
        downloads = aria2.get_downloads()
        await asyncio.sleep(3)
        aria2.remove(downloads, force=True, files=True, clean=True)
        ARIA2.append(aria2)

        # return aria2

    except Exception:
        await logger(Exception, critical=True)
        # return None


async def start_rpc():
    os.system(
        f"aria2c --enable-rpc=true --rpc-max-request-size=1024M --rpc-listen-port={ARIA2_PORT} --seed-time=0 --follow-torrent=mem --summary-interval=0 --daemon=true --allow-overwrite=true"
    )
    await asyncio.sleep(3)
    await start_aria2p()


async def onrestart():
    try:
        if sys.argv[1] == "restart":
            msg = "**Restarted!** "
        elif sys.argv[1].startswith("update"):
            s = sys.argv[1].split()[1]
            if s == "True":
                with open(version_file, "r") as file:
                    v = file.read()
                msg = f"**Updated to >>>** `{v}`"
            else:
                msg = "**No major update found!**\n" f"`Bot restarted! {enmoji()}`"
        else:
            return
        chat_id, msg_id = map(int, sys.argv[2].split(":"))
        await pyro.edit_message_text(chat_id, msg_id, msg)
    except Exception:
        await logger(Exception)


async def onstart():
    try:
        for i in OWNER.split():
            try:
                await tele.send_message(int(i), f"**I'm {enquip()} {enmoji()}**")
            except Exception:
                pass
        if LOG_CHANNEL:
            me = await pyro.get_users("me")
            await tele.send_message(
                LOG_CHANNEL, f"**{me.first_name} is {enquip()} {enmoji()}**"
            )
    except BaseException:
        pass


async def on_termination():
    try:
        dead_msg = f"**I'm {enquip2()} {enmoji2()}**"
        if LOG_CHANNEL:
            await tele.send_message((LOG_CHANNEL), dead_msg)
        else:
            for i in OWNER.split():
                try:
                    await tele.send_message(int(i), dead_msg)
                except Exception:
                    pass
    except Exception:
        pass
    # More cleanup code?
    exit(0)


async def on_startup():
    # if not STARTUP:
    try:
        asyncio.create_task(autostat())
        asyncio.create_task(start_rpc())
        loop = asyncio.get_running_loop()
        for signame in {"SIGINT", "SIGTERM", "SIGABRT"}:
            loop.add_signal_handler(
                getattr(signal, signame),
                lambda: asyncio.create_task(on_termination()),
            )
        if len(sys.argv) == 3:
            await onrestart()
        else:
            await onstart()
        await entime.start()
        await asyncio.sleep(30)
        asyncio.create_task(something())
    except Exception:
        logger(Exception)
    startup_.append(1)
    # STARTUP.append(1)
