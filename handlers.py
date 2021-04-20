import logging
import random

import youtubequicksearch
import smesharikimirparse
from smesharikimirparse import VideoPageParser, SmesharikiMirException
from fandomparse import FandomParser, FandomParserException

EPISODE_START_TIMECODE = 21

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)


class HandlersException(Exception):
    pass


def start(update, context):
    update.message.reply_text("Барабудай рабубиру будай...")


def get_help(update, context):
    update.message.reply_text(
        "/flat <i>n</i> — узнать что-то про <i>n</i>-ю серию "
        "2D-смешариков\n"
        "/3d <i>n</i> — то же для 3D\n"
        "/random — то же для случайной серии\n", parse_mode="HTML"
    )


def echo(update, context):
    if update.message.text.endswith((".", "?", "!")):
        response = update.message.text + update.message.text[-1] * 2
    else:
        response = update.message.text + random.choice(
            ["?", "???", "?!", "...", ".", "!!!"])

    update.message.reply_text(response)


def get_episode_info(update, context, episode_list_parser):
    try:
        episode_number = extract_episode_number_from_args(context,
                                                          episode_list_parser)
    except HandlersException as exception:
        update.message.reply_text(str(exception), parse_mode="HTML")
        return

    chat_message = update.message.reply_text(random.choice(
        ["Щас все будет...", "Уже ищу...", "Происходит поиск.", "Минутку..."]))

    message_text = episode_info_string(episode_list_parser, episode_number)
    chat_message.edit_text(message_text[:4096], parse_mode="HTML")
    for chunk in range(4096, len(message_text), 4096):
        update.message.reply_text(message_text[chunk:chunk + 4096],
                                  parse_mode="HTML")


def get_flat_info(update, context):
    get_episode_info(update, context, smesharikimirparse.oldEpisodesListParser)


def get_3d_info(update, context):
    get_episode_info(update, context, smesharikimirparse.newEpisodesListParser)


def random_ep_info(update, context):
    if bool(random.getrandbits(1)):
        get_flat_info(update, context)
    else:
        get_3d_info(update, context)


def error(update, context):
    logger.warning("Update '%s' caused error '%s'", update, context.error)


def episode_info_string(episode_list_parser, episode_number):
    episode_name = episode_list_parser.get_episode_name(episode_number)
    episode_description = episode_list_parser.get_episode_description(
        episode_number)

    try:
        video_page_index = episode_list_parser.get_episode_video_page_index(
            episode_number)
        video_page_parser = VideoPageParser(video_page_index)
        video_link = video_page_parser.get_video_link(EPISODE_START_TIMECODE)
    except SmesharikiMirException:
        video_link = "В общей базе не нашлось ссылки на эту серию, " \
                     "зато вот первый результат поиска на YouTube: "
        video_link += youtubequicksearch.searcher.get_youtube_video_url(
            "смешарики " + episode_name, EPISODE_START_TIMECODE)

    info_string = "<u><b>{}</b></u>\n\n<i>{}</i>\n".format(
        episode_name, episode_description)

    fandom_parser = FandomParser(episode_name)
    sections_to_grab = ["Интересные факты", "Ляпы", "Интересные факты и ляпы"]
    for section in sections_to_grab:
        try:
            section_list = fandom_parser.get_section_list(section)
            if len(section_list) != 0:
                info_string += "\n<b>{}:</b>\n".format(section) + "• " + \
                               "\n• ".join(section_list) + "\n"
        except FandomParserException:
            pass

    info_string += "\n" + video_link

    return info_string


def extract_episode_number_from_args(context, episode_list_parser):
    if len(context.args) == 0:
        return random.randint(1, episode_list_parser.episodes_count())

    try:
        episode_number = int(context.args[0])
    except ValueError:
        raise HandlersException(
            "Введите номер эпизода, а не <i>\"{}\"</i>, пожалуйста".format(
                " ".join(context.args).strip()))

    if episode_number > episode_list_parser.episodes_count():
        raise HandlersException(
            "Серий всего лишь {}, к сожалению".format(
                episode_list_parser.episodes_count()))
    elif episode_number <= 0:
        raise HandlersException(
            "Да я и сам уже не человек, а зверь из-за этих отрицательных чисел"
        )

    return episode_number
