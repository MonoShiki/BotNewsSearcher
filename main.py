

import cfg
import mysoup as fss
import logging
from aiogram import Bot, Dispatcher, executor,types
import asyncio
import cfg as c
import aiogram.utils.markdown as fmt

db_post = cfg.db_post
chat_id = cfg.chat_id
TOKEN = cfg.TOKEN
bot = Bot(token=c.TOKEN)
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)

@dp.message_handler(content_types="text")
async def brain(message):
    await dp.bot.send_message(message.chat.id,f"Твой айди: {message.chat.id}")

@dp.message_handler(commands=["start"])
async def aboba():
    await bot.get_chat_member(chat_id,chat_id)

async def posting_information():
    old_posts = db_post.get_all_posts()
    soup_object = fss.MySoup()
    dict_of_posts = await soup_object.download()
    list_posts = []
    for key in dict_of_posts:
        href = dict_of_posts[key]["href"]
        if href in old_posts:
            continue
        post = f"{dict_of_posts[key]['date']}\n{dict_of_posts[key]['text']}\n{fmt.hlink('Подробнее', href)}\n\n@mospolitech"
        list_posts.append({"href": href, "text": dict_of_posts[key]['text'], "img": dict_of_posts[key]["img"],
                           "date": dict_of_posts[key]['date']})
        try:
            await dp.bot.send_photo(chat_id, photo=dict_of_posts[key]["img"], caption=post, parse_mode="HTML")
        except Exception as e:
            print(f"Ошибка с фотографией \n{e}")
            img_for_err = "https://mospolytech.ru//upload/iblock/b21/9abd0c7b-8888-466f-95f5-0f9f89356a84.jpg"
            await dp.bot.send_photo(chat_id, photo=img_for_err, caption=post, parse_mode="HTML")
        return list_posts


async def scheduled(wait_for):
    while True:
        await asyncio.sleep(wait_for)
        my_list = await posting_information()
        if my_list:
            for post in my_list:
                db_post.add_post(post["href"], post["text"], post["img"], post["date"])

async def on_startup(_):
    asyncio.create_task(scheduled(10))


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)
