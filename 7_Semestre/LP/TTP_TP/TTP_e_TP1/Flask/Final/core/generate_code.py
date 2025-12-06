import qrcode

def get_qr_code(dados:str): # 1. Recebe Dados para o QR code

    # 2. Criação do objeto QR code
    img_data = qrcode.make(dados)

    # 3. Retorna o QR code para o solicitante
    return img_data

# se quiser rodar e testar localmente
#image=get_qr_code("https://github.com/kasshinokun/Q3_Q4_2025_Public/tree/main/7_Semestre/LP/TTP_TP")
#image.save("image.png")