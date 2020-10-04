from channels.consumer import SyncConsumer

from asgiref.sync import async_to_sync
from django.contrib.auth.models import User
from chat.models import Thread,Message
import json
class ChatConsumer(SyncConsumer):
    def websocket_connect(self,event):
        username1=self.scope.get('user')
        me =User.objects.get(username=username1)
        other_username=str(self.scope['url_route']['kwargs']['username'])
        other_user=User.objects.get(username=other_username)
        self.thread_obj=Thread.objects.get_or_create_personal_thread(me,other_user)
        self.room_name=f'peronal_thread_{self.thread_obj.id}'    
        async_to_sync(self.channel_layer.group_add)(self.room_name,self.channel_name)
        self.send({
            'type':'websocket.accept'
        })
        print(f'{self.channel_name} - you are connected')
    def websocket_receive(self,event):
        # print('New event is recieved')

        msg =json.dumps({
            'text':event.get('text'),
            'username':self.scope['user'].username
        })
        self.store_message(event.get('text'))
        print(f'[{self.channel_name}] - Recieved_message -  {event["text"]}')
        # print(event)
        async_to_sync(self.channel_layer.group_send)(
            self.room_name,
            {
                'type':'websocket.message',
                'text':msg 
            }
        )
        # self.send({
        #     'type':'websocket.send',
        #     'text':event.get('text')
        # })
    def websocket_message(self,event):
        print(f'[{self.channel_name}] - message sent-  {event["text"]}')    
        self.send({
            'type':'websocket.send',
            'text':event.get('text')
        })
    def websocket_disconnect(self,event):
        print(f'[{self.channel_name}] -disconnected')    
        async_to_sync(self.channel_layer.group_discard)(self.room_name,self.channel_name)
        print(event)
    def store_message(self,text):
        Message.objects.create(
            thread =self.thread_obj,
            sender=self.scope["user"],
            text=text
        )

class EchoConsumer(SyncConsumer):
    def websocket_connect(self,event):
        self.room_name='broadcast'
        # print('connect event is called')
        
        self.send({
            'type':'websocket.accept'
        })
        async_to_sync(self.channel_layer.group_add)(self.room_name,self.channel_name)
        print(f'{self.channel_name} - you are connected')
    def websocket_receive(self,event):
        # print('New event is recieved')
        print(f'[{self.channel_name}] - Recieved_message -  {event["text"]}')
        # print(event)
        async_to_sync(self.channel_layer.group_send)(
            self.room_name,
            {
                'type':'websocket.message',
                'text':event.get('text')
            }
        )
        # self.send({
        #     'type':'websocket.send',
        #     'text':event.get('text')
        # })
    def websocket_message(self,event):
        print(f'[{self.channel_name}] - message sent-  {event["text"]}')    
        self.send({
            'type':'websocket.send',
            'text':event.get('text')
        })
    def websocket_disconnect(self,event):
        print(f'[{self.channel_name}] -disconnected')    
        async_to_sync(self.channel_layer.group_discard)(self.room_name,self.channel_name)
        print(event)