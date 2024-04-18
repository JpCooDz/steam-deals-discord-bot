import requests
from bs4 import BeautifulSoup
import discord
from discord.ext import commands

bot = commands.Bot(command_prefix='/')

@bot.command(name='promocao_steam')
async def steam_sale(ctx):
    res = requests.get('https://store.steampowered.com/search/?specials=1')
    soup = BeautifulSoup(res.content, 'html.parser')
    games = soup.find_all('a', {'class': 'search_result_row'})

    embed = discord.Embed(title="Promoções Steam")
    for game in games[:20]:
        name = game.find('span', {'class': 'title'}).text
        original_price_element = game.find('div', {'class': 'discount_original_price'})
        original_price = original_price_element.text.strip() if original_price_element else 'Preço não disponível'
        discount_price_element = game.find('div', {'class': 'discount_final_price'})
        discount_price = discount_price_element.text.strip() if discount_price_element else 'Preço não disponível'

        embed.add_field(name=name, value=f"Preço Original: {original_price}\nPreço com Desconto: {discount_price}", inline=False)
    
    await ctx.send(embed=embed)


@bot.command(name='promocao_epic')
async def epic_sale(ctx):
    res = requests.get('https://store-site-backend-static.ak.epicgames.com/freeGamesPromotions?locale=pt-BR&country=BR&allowCountries=BR')
    data = res.json()['data']['Catalog']['searchStore']['elements']
    games = [game for game in data if game['price']['totalPrice'] != 0][:20]

    embed = discord.Embed(title="Promoções Epic Games")
    for game in games:
        title = game['title']
        original_price = game['price']['totalPrice']['fmtPrice']['originalPrice']
        discount_price = game['price']['totalPrice']['fmtPrice']['discountPrice']

        embed.add_field(name=title, value=f"Preço Original: {original_price}\nPreço com Desconto: {discount_price}", inline=False)
    
    await ctx.send(embed=embed)

TOKEN = 'seu_token_aqui'
bot.run(TOKEN)
