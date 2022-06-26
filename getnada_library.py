from robot.api.deco import keyword
from robot.libraries.BuiltIn import BuiltIn
from bs4 import BeautifulSoup
from lxml import html
import requests
import os
import uuid

ROBOT_LIBRARY_DOC_FORMAT = 'reST'

api = 'https://getnada.com/api/v1'


@keyword(name='Get MailBox')
def get_mailbox(
    mail: str,
    tittle: str = '', 
    author: str = ''
):
    """
    Retorna a caixa de entrada de um email pertencente ao

    https://getnada.com/

    ***** Nescessario informar um **Email**.\n
    **-** pode filtrar por author do email pelo argumento **author**\n
    **-** pode filtrar pelo titulo atravez do argumento **tittle**
    """

    url = f'{api}/inboxes/{mail}'
    response = requests.get(url).json()['msgs']

    if author != '':
        response = [m for m in response if author in m['fe']]

    if tittle != '':
        response = [m for m in response if tittle in m['s']]

    print(response)
    return response


@keyword(name='Has Attachments')
def has_attachments(
    message_id: str
):
    """
    Retorna um valor **Verdadeiro** ou **Falso**
    caso tenha ou não anexos em uma mensagem.

    ***** Nescessario informar um **ID** de uma mensagem.
    """

    result = []

    if message_id != '':
        result = requests.get(f'{api}/messages/{message_id}').json()['at']

    result = len(result) > 0

    print(result)
    return result


@keyword(name='Get Attachments')
def get_attachments(
    message_id: str
):
    """
    Retorna os anexos de uma mensagem

    ***** Nescessario informar um **ID** de uma mensagem.
    """

    result = []

    if message_id != '':
        result = requests.get(f'{api}/messages/{message_id}').json()['at']

    print(result)
    return result


@keyword(name='Download Attachment')
def download_attachment(
    message_id: str,
    attachment: dict,
    path: str = ''
):
    """
    Realiza o Download de um anexo

    ***** Nescessario informar um **ID** de uma mensagem.\n
    ***** Nescessario informar um **ID** de um anexo.\n
    **-** Nescessario informar o caminho onde deve ser baixado para alterar o caminho (padrão dentro do output_dir).
    """

    url = f'{api}/file/{message_id}/{attachment["uid"]}'
    if path == '':
        path = BuiltIn().get_variable_value(name='${OUTPUT_DIR}')
    file = os.path.join(path, attachment["name"])

    print(f'Salvando Anexo do link: \n{url}')
    response = requests.get(url).content

    with open(file, 'wb') as f:
        f.write(response)

    print(f'\nArquivo baixado: \n{file}')

    return file


@keyword(name='Generate Random Mail')
def generate_random_mail():
    """
    Cria um email valido para o **GetNada**
    """

    id = str(uuid.uuid4()).replace('-', '')[0:22]

    return f"5870@getnada.com".lower()


@keyword(name='Get Raw Message')
def get_raw_message(
    message_id: str,
    xpath: str = '',
    attribute_name: str = ''
):
    """
    Retorna o conteudo de uma mensagem

    **-** Podendo filtar por **Xpath** para retornar um texto expecifico\n
    **-** Junto com o **Xpath** caso seja passado um atributo então é retornado um valor de um atributo
    """

    url = f'{api}/messages/html/{message_id}'
    content = requests.get(url).text

    if xpath != '':
        soup = BeautifulSoup(content, features="html.parser")
        tree = html.fromstring(soup.__str__())
        if attribute_name == '':
            if len(tree.xpath(xpath)) > 1:
                for i in tree.xpath(xpath):
                    content = content + i.text + '\n'
            else:
                content = tree.xpath(xpath)[0].text
        else:
            content = tree.xpath(xpath)[0].attrib[attribute_name]

    print(content)
    return content
