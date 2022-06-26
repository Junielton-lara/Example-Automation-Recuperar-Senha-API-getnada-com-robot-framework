*** Settings ***
Library  getnada_library.py
Library    XML
Library    SeleniumLibrary
Library    openpyxl

*** Test Cases ***
Fluxo E-mail Login
  ${mail}  Generate Random Mail
  Log To Console  Email criado: ${mail}

  ${response}  Get MailBox  
  ...  mail=exemplo@getnada.com
  ...  tittle=Exemplo titulo do email
  Log To Console    tittle:${response}
  ${content}  Get Raw Message
  ...  message_id=${response[0]['uid']}
  ...  xpath=//a[contains(text(),'Clique Aqui')]
  ...  attribute_name=href
  Log To Console    ${content}

    
    # Open Browser     browser=chrome
    # Go To    ${content}
    # Wait Until Element Is Visible    id=NewPassword
    # Input Password    id=NewPassword    senha@123
    # Input Password    id=NewPasswordConfirm    senha@123
    # Click Element     //*[@id="btnEnviar"]/span[1]
    
    #  ${status}  Run Keyword And Return Status    Wait Until Page Contains  Senha alterada com sucesso
    #          IF  ${status}    
    #              Log    Senha alterada com sucesso
    #              Log To Console    Senha alterada com sucesso
    #                 ELSE
    #                 Log    Falha na troca da senha
    #                 Log To Console    Falha na troca da senha
    #              END