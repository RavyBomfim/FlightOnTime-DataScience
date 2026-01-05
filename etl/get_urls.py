def get_urls() -> list:
    """
    Gera a lista completa de URLs dos arquivos CSV do conjunto 
    “Voo Regular Ativo (VRA)” disponibilizado pela ANAC.

    A função constrói dinamicamente os caminhos de acesso aos arquivos 
    organizados por ano e mês, conforme a estrutura oficial do portal de 
    dados abertos da ANAC. São consideradas todas as combinações entre os anos 
    de 2000 a 2025 e os 12 meses do ano, com exceção dos meses posteriores a 
    outubro de 2025, pois esses arquivos ainda não estão disponíveis.

    Para cada combinação válida, é gerada a URL correspondente no formato:
        https://.../ANO/MM - Mês/VRA_ANOMM.csv

    Retorna uma lista contendo todas as URLs resultantes, na ordem cronológica.

    Retorno
    -------
    list
        Lista de strings contendo as URLs completas dos arquivos CSV do VRA.
    """

    url_base = "https://sistemas.anac.gov.br/dadosabertos/Voos%20e%20opera%C3%A7%C3%B5es%20a%C3%A9reas/Voo%20Regular%20Ativo%20%28VRA%29"
    anos = list(range(2018, 2026))
    meses = {
        1:  "01%20-%20Janeiro",
        2:  "02%20-%20Fevereiro",
        3:  "03%20-%20Mar%C3%A7o",
        4:  "04%20-%20Abril",
        5:  "05%20-%20Maio",
        6:  "06%20-%20Junho",
        7:  "07%20-%20Julho",
        8:  "08%20-%20Agosto",
        9:  "09%20-%20Setembro",
        10: "10%20-%20Outubro",
        11: "11%20-%20Novembro",
        12: "12%20-%20Dezembro"
    }

    urls = []

    for ano in anos:
        for mes in meses.items():
            if ano == 2025 and mes[0] > 10:
                continue
            url = f"{url_base}/{ano}/{mes[1]}/VRA_{ano}{mes[0]}.csv"
            urls.append(url)
    
    return urls