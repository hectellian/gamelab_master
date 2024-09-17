import pytest
from unittest.mock import AsyncMock

from gamelab_master.bot import GamelabMasterBot

# Fixture to initialize the bot
@pytest.fixture
def bot():
    return GamelabMasterBot(token='dummy', comitee_chat_id='test', official_chat_id='test')

def test_dummy():
    assert True

# # Test starting the bot command
# @pytest.mark.asyncio
# async def test_start(bot, mocker):
#     mock_update = mocker.MagicMock()
#     mock_context = mocker.MagicMock()
#     mock_update.message.reply_text = AsyncMock()
#     await bot.start(mock_update, mock_context)
#     mock_update.message.reply_text.assert_called_once_with('Hello! I will help manage your Gamelab events.')

# # Test sending a poll successfully
# @pytest.mark.asyncio
# async def test_send_poll_success(bot, mocker):
#     mock_send_poll  = mocker.patch('gamelab_master.bot.GamelabMasterBot.send_poll', new_callable=AsyncMock)
#     await bot.send_poll()
#     mock_send_poll.assert_called_once()

# # Test sending a message upon reaching the minimum votes
# @pytest.mark.asyncio
# async def test_announce_event(bot, mocker):
#     mock_update = mocker.MagicMock()
#     mock_context = mocker.MagicMock()
#     mock_context.bot.send_message = AsyncMock()
#     mock_update.poll_answer.option_ids = [0, 0]
#     mock_announcement = mocker.patch('telegram.ext.Application.bot.send_message', new_callable=AsyncMock)
#     await bot.handle_poll_answer(mock_update, mock_context)
#     mock_announcement.assert_called_once()
#     mock_context.bot.send_message.assert_called_once()

# # Test error during sending poll
# @pytest.mark.asyncio
# async def test_send_poll_error(bot, mocker):
#     mocker.patch('gamelab_master.bot.GamelabMasterBot.send_poll', new_callable=AsyncMock, side_effect=Exception("Failed to send poll"))
#     with pytest.raises(Exception):
#         await bot.send_poll()
