
from entities.message import Message
from notification.discord import Discord

discordInstance = Discord("https://discordapp.com/api/webhooks/1351560228147167262/zhmZJacoissnC_ux-WuLHqfg8DrnS9Q8yxDnyBKAJJKkhiOrSFH_NQwIFQ-6MkqWB-kI")

message = Message("Castrol", "Status code 500 ao tentar realizar busca de produtos")

discordInstance.send(message)