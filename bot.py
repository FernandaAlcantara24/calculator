from telegram import Update, InputFile
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from db import init_db, adicionar_gasto, obter_gastos_mes, limpar_tudo, limpar_categoria
from grafico import gerar_grafico

init_db()

async  def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Olá, Me envie suas despesas da seguinte forma: \n\n`Mercado 120.50`\n\n"
        "Use /resumo para ver o total do mês.\n"
        "Use /grafico pizza ou /grafico barras para gerar gráfico.\n"
        "Use /ajuda para mais comandos."
        "Use /limpar para limpar *TODOS* os dados"
        "Use /limparCategoria para limpar a categoria",
        parse_mode="Markdown"
    )

async def ajuda(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Formatos suportados:\n\n"
                                    "`Mercado 25.50`\n"
                                    "/resumo → ver total por categoria\n"
                                    "/grafico pizza → gráfico de pizza\n"
                                    "/grafico barras → gráfico de barras\n"
                                    "/limpar → Limpar *TODOS* os dados\n"
                                    "/limparCategoria → Limpar apenas a categoria desejada. Exemplo de uso:\n `/limpar `Mercado` `",
                                    parse_mode="Markdown"
                                    )

async def registrar_gasto(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        partes = update.message.text.strip().split()
        categoria = partes[0]
        valor = float(partes[1])
        user_id = update.message.from_user.id
        adicionar_gasto(user_id, categoria, valor)
        await  update.message.reply_text(f"{categoria} R${valor:.2f} Adicionado!")
    except Exception as e:
        await update.message.reply_text("Formato inválido. Exemplo: `Transporte-Ônibus 20.50`",  parse_mode="Markdown")

async def resumo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    dados = obter_gastos_mes(user_id)
    if not dados:
        await update.message.reply_text("Nenhum gasto registrado este mês.")
        return
    resposta = "📊 *Resumo do mês:*\n"
    total = 0
    for categoria, valor in dados:
        resposta += f"• {categoria}: R${valor:.2f}\n"
        total += valor
    resposta += f"\n💰 *Total:* R${total:.2f}"
    await update.message.reply_text(resposta, parse_mode="Markdown")

async def grafico(update: Update, context: ContextTypes.DEFAULT_TYPE):
    tipo = context.args[0] if context.args else 'pizza'
    user_id = update.message.from_user.id
    dados = obter_gastos_mes(user_id)
    if not dados:
        await update.message.reply_text('Sem dados para gerar gráfico.')
        return
    try:
        caminho = "grafico.png"
        gerar_grafico(dados, tipo, caminho)
        with open(caminho, "rb") as f:
            await update.message.reply_photo(photo=InputFile(f))
    except Exception as e:
        await update.message.reply_text("Erro ao gerar gráfico. Use `/grafico pizza` ou `/grafico barras.`")

async def limpar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    if context.args:
        categoria = context.args[0]
        limpar_categoria(user_id, categoria)
        await update.message.reply_text(f"🧹 Gastos da categoria '{categoria}' removidos.")
    else:
        limpar_tudo(user_id)
        await  update.message.reply_text("🧹 Todos os seus gastos foram apagados.")

if __name__ == "__main__":
    from os import getenv
    import  asyncio

    TOKEN = ""
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("ajuda", ajuda))
    app.add_handler(CommandHandler("resumo", resumo))
    app.add_handler(CommandHandler("grafico", grafico))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), registrar_gasto))
    app.add_handler(CommandHandler("limpar", limpar))

    print("Bot iniciado...")
    app.run_polling()
