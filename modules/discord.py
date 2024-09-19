from discord_webhook import DiscordWebhook

from discord_webhook import DiscordWebhook, DiscordEmbed

# URL del webhook de Discord
webhook_url = 'https://discordapp.com/api/webhooks/1285221021720252467/mzuX_8A9MQGjjgAF80D_CpZ_Z39a0f5nVW6FzAP8P6w_Jue-V5urfkEG8cXdyQk8_3Zo'

# Crea el webhook con contenido personalizado
webhook = DiscordWebhook(
    url=webhook_url, 
    username="Bot Personalizado", 
    #avatar_url="https://i.imgur.com/AfFp7pu.png"
)

# Crear un embed (mensaje enriquecido)
embed = DiscordEmbed(
    title="Título del Embed", 
    description="Descripción del mensaje enriquecido", 
    color=0x00ff00  # Color verde
)

# Añadir campos al embed
embed.add_embed_field(name="Campo 1", value="Valor del campo 1")
embed.add_embed_field(name="Campo 2", value="Valor del campo 2")

# Adjuntar el embed al webhook
webhook.add_embed(embed)

# Envía el webhook con el embed
response = webhook.execute()

if response.status_code == 200:
    print("Mensaje con embed enviado con éxito.")
else:
    print(f"Error al enviar el mensaje: {response.status_code}")
