import streamlit as st
from core import Extractor
from PIL import Image


def main():
    st.title('Extrator de placas veiculares')
    st.markdown("""
        ### Instruções
    
        Faça o upload de uma imagem e clique em **processar**. 
        
        Nós tentaremos extrair **somente** a placa. (utilizaremos como base o padrão mercosul)
    """)
    st.info('Para um melhor resultado, recomendamos enviar imagens em alta resolução')

    image_file = st.file_uploader("Envie a imagem", type=['png', 'jpg', 'jpeg'])

    if image_file:
        image = Image.open(image_file)

        if st.button("Processar"):
            extractor = Extractor(image)
            extracted = extractor()
            if extracted is not None:
                st.text("Placa extraída da imagem:")
                st.image(extracted)
            else:
                st.error('Não conseguimos extrair a placa')
    else:
        st.text('Faça o upload de uma imagem')


if __name__ == '__main__':
    main()
