from gql import gql, Client, WebsocketsTransport
from secret import TOKEN, ADVENTURE_ID

_transport = WebsocketsTransport(
    url='wss://api.aidungeon.io/subscriptions',
    init_payload={"token":"d44e46bc-11e8-4a5c-a0c6-6031bf0901ef"} #auth token, use login() mutation to obtain
)

client = Client(
    transport=_transport,
    fetch_schema_from_transport=True,
)


adventure_id = ADVENTURE_ID #obtain from the URL while playing an adventure
class AID: 
  
  @staticmethod
  def getAIResponse():
    variables = {
      "publicId": adventure_id
    }
    lastActionQuery = gql("""
    query ($publicId: String!) {
      adventure(publicId: $publicId) {
           lastAction {
              text
           }
     }
    }
   """
  )
    return client.execute(lastActionQuery, variable_values=variables).get('adventure').get('lastAction').get('text')
  @staticmethod
  def sendAction(text, type): # type == "do" || "say" || "story" 
    variables = {
      "text": text,
      "publicId": adventure_id,
      "type": type
    }
    sendActionQuery = gql("""
    mutation ($publicId: String!, $text: String!, $type: String!) {
      addAction(input: {publicId: $publicId, type:$type, text: $text, characterName: "You"}) {
      message 
    }
    }
    """) #should return None if everything is alright
    return client.execute(sendActionQuery, variable_values=variables)
  @staticmethod
  def getQuests():
    variables = {
      "publicId": adventure_id
    }
    getQuestsQuery = gql("""
    query ($publicId: String!){
      adventure(publicId: $publicId) {
        quests {
          text
          completed
        }
      }
    }
    """) 
    result = client.execute(getQuestsQuery, variable_values=variables).get('adventure').get('quests')
    quests = []
    for q in result:
      if (q.get('completed')==False): quests.append(q.get('text'))
    return quests
  @staticmethod
  def getMemory():
    variables = {
      "publicId": adventure_id
    }
    getMemoryQuery = gql("""
    query ($publicId: String!){
      adventure(publicId: $publicId) {
        memory
      }
    }
    
    """)
    return client.execute(getMemoryQuery, variable_values=variables).get('adventure').get('memory')
  @staticmethod
  def remember(text):
    variables = {
      "input": {"publicId": adventure_id, "memory": AID.getMemory()+text}
    }
    rememberQuery = gql("""
    mutation ($input: MemoryInput!){
      updateAdventureMemory(input: $input) {
        id
      }
    }
    """
    )
    return client.execute(rememberQuery, variable_values=variables)

#print(AID.getAIResponse())                                 #examples
#print(AID.sendAction("look at the next page", "do"))
#print(AID.remember("asdasdasd"))
#print(AID.getMemory())
