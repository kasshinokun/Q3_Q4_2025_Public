import qrcode
import base64

def get_qr_code(dados:str): # 1. Recebe Dados para o QR code

    # 2. Criação do objeto QR code
    img = qrcode.make(dados)

    buffered = BytesIO()
    img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()

    # 3. Retorna o QR code para o solicitante em base64 
    return f"data:image/png;base64,{img_str}"
    # return img_data

# se quiser rodar e testar localmente
#image=get_qr_code("https://github.com/kasshinokun/Q3_Q4_2025_Public/tree/main/7_Semestre/LP/TTP_TP")
#image.save("image.png")
