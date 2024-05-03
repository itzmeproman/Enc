async def another(text, title, epi, sea, metadata, dl):
    a_auto_disp = "-disposition:a auto"
    s_auto_disp = "-disposition:s auto"
    a_pos_in_stm, s_pos_in_stm = await pos_in_stm(dl)

    if title:
        if "This Episode" in text:
            info = title
            if epi:
                info = f"Episode {epi} of {title}"
            if sea:
                info += f" Season {sea}"
            text = text.replace(f"This Episode", info)

    if "Fileinfo" in text:
        text = text.replace(f"Fileinfo", metadata)
    if a_auto_disp in text:
        if a_pos_in_stm or a_pos_in_stm == 0:
            text = text.replace(
                a_auto_disp,
                f"-disposition:a 0 -disposition:a:{a_pos_in_stm} default",
            )
        else:
            text = text.replace(a_auto_disp, "-disposition:a 0")
    if s_auto_disp in text:
        if s_pos_in_stm or s_pos_in_stm == 0:
            text = text.replace(
                s_auto_disp,
                f"-disposition:s 0 -disposition:s:{s_pos_in_stm} default",
            )
        else:
            text = text.replace(s_auto_disp, "-disposition:s 0")
    return text


async def forward_(name, out, ds, mi, f):
    fb = conf.FBANNER
    fc = conf.FCHANNEL
    fs = conf.FSTICKER
    if not fc:
        return
    try:
        pic_id, f_msg = await f_post(name, out, conf.FCODEC, mi, _filter=f, evt=fb)
        if pic_id:
            await pyro.send_photo(photo=pic_id, caption=f_msg, chat_id=fc)
    except Exception:
        await logger(Exception)
    await ds.copy(chat_id=fc)
    if not fs:
        return
    if not fb:
        queue = get_queue()
        bqueue = get_bqueue()
        queue_id = list(queue.keys())[0]
        if bqueue.get(queue_id):
            name, _none, v_f = list(queue.values())[0]
            blist = await get_batch_list(einfo._current, 1, v_f[0], v_f[1], parse=False)
            if blist:
                _pname = await qparse_t(einfo._current, v_f[0], v_f[1])
                _pname2 = await qparse_t(blist[0], v_f[0], v_f[1])
                if _pname == _pname2:
                    return

        elif len(queue) > 1:
            name, _none, v_f = list(queue.values())[0]
            name2, _none, v_f2 = list(queue.values())[1]
            _pname = await qparse_t(name, v_f[0], v_f[1])
            _pname2 = await qparse_t(name2, v_f2[0], v_f2[1])
            if _pname == _pname2:
                return
    try:
        await pyro.send_sticker(
            fc,
            sticker=fs,
        )
    except Exception:
        await logger(Exception)


def skip(queue_id):
    if einfo.batch:
        return
    bqueue = get_bqueue()
    queue = get_queue()
    try:
        bqueue.pop(queue_id)
    except Exception:
        pass
    try:
        queue.pop(queue_id)
    except Exception:
        pass


async def something():
    while True:
        await thing()
        # do some other stuff?


async def thing():
    try:
        while get_var("pausefile"):
            await asyncio.
