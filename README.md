# Web Scraper e Análise de Vagas de Emprego

Este projeto tem como objetivo buscar vagas de emprego na plataforma Catho, extrair informações relevantes e gerar relatórios sobre as oportunidades encontradas.

## Funcionalidades

- Busca automática de vagas com base em palavras-chave fornecidas pelo usuário.
- Extração de dados como título da vaga, empresa, localização, data de publicação, faixa salarial e descrição.
- Análise de frequência de palavras-chave e tecnologias mencionadas nas descrições das vagas.
- Geração de relatório com insights sobre habilidades mais requisitadas e experiência exigida.
- Uso da API da OpenAI para obter insights adicionais sobre o mercado de trabalho.

## Tecnologias Utilizadas

- **Python**
- **Selenium** para web scraping
- **Pandas** para manipulação de dados
- **OpenAI API** para análise de insights
- **CSV** para armazenamento de dados
- **Regex** para extração de informações relevantes

## Requisitos

Certifique-se de ter as bibliotecas necessárias instaladas antes de executar o projeto:

```bash
pip install selenium pandas openai webdriver-manager
```

Também é necessário ter o ChromeDriver instalado, que pode ser gerenciado automaticamente pelo WebDriver Manager.

## Como Usar

1. **Executar o script:**

   ```bash
   python script.py
   ```

2. **Fornecer o tipo de vaga desejada** quando solicitado.

3. **Aguarde a coleta dos dados.** As informações serão armazenadas em `vagas.csv`.

4. **O script também irá gerar um relatório** com insights em `relatorio_insights.txt`.

## Saída dos Dados

- `vagas.csv`: Contém todas as vagas coletadas com os seguintes campos:
  - Título
  - Empresa
  - Localização
  - Data de publicação
  - Faixa salarial
  - Descrição
  - URL da vaga

- `relatorio_insights.txt`: Relatório com análise descritiva e insights sobre habilidades mais demandadas.

## Observações

- O uso da API da OpenAI requer uma chave válida.
- Como o site da Catho pode mudar, é possível que seletores precisem ser ajustados.
- Certifique-se de respeitar os Termos de Uso do site ao realizar scraping.

## Autor

Este projeto foi desenvolvido para auxiliar na análise de oportunidades de trabalho na área de tecnologia.

