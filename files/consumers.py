import asyncio
import json
from django.contrib.auth import get_user_model
from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async

from .models import File, Comment
from django.contrib.auth import get_user_model

User = get_user_model()


class CommentConsumer(AsyncConsumer):
    async def websocket_connect(self, event):
        await self.send({
            'type': 'websocket.accept'
        })
        room_slug = await self.get_file_id(self.scope['url_route']['kwargs']['id'])
        self.room = room_slug
        await self.channel_layer.group_add(
            self.room,
            self.channel_name,
        )

    async def websocket_receive(self, event):
        print('receive', event)
        new_comment_data = event.get('text')
        new_comment = json.loads(new_comment_data)
        user_id = new_comment['author']
        user = User.objects.get(id=int(user_id))
        print('makaka',user)
        comment_text = new_comment['comment_text']
        file_id = new_comment['file_id']
        message = await self.create_comment(user_id, comment_text, file_id)
        comment = {
            'comment_text': comment_text,
            'username': user.username,
        }
        await self.channel_layer.group_send(
            self.room,
            {
                'type': 'show_comment',
                'text': json.dumps(comment),
            }
        )

    async def websocket_disconnect(self, event):
        print('disconnected', event)

    @database_sync_to_async
    def get_file_id(self, file_id):
        return str(File.objects.get(id=int(file_id)).id)

    @database_sync_to_async
    def create_comment(self, user_id, comment_text, file_id):
        author = User.objects.get(id=user_id)
        file = File.objects.get(id=file_id)
        message = Comment(
            users=author,
            content = comment_text,
            files=file,
        )
        message.save()
        return message

    async def show_comment(self, event):
        await self.send({
            'type': 'websocket.send',
            'text': event['text'],
        })