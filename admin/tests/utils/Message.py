from django.contrib.messages import get_messages


class Message:
    @staticmethod
    def getMessages(response) -> list:
        messages = []
        for message in get_messages(response.wsgi_request):
            messages.append(str(message))
        return messages