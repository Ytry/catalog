from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
 
from database_setup import Category, Base, Item
 
engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine
 
DBSession = sessionmaker(bind=engine)
session = DBSession()

# make categories

category1 = Category(name="Produce")
session.add(category1)
session.commit()

category2 = Category(name="Meat")
session.add(category2)
session.commit()

category3 = Category(name="Bread")
session.add(category3)
session.commit()

category4 = Category(name="Dairy")
session.add(category4)
session.commit()

# add items to categories

broccoli = Item(name="Broccoli", category=category1, description="Broccoli is an edible green plant in the cabbage family whose large flowerhead is eaten as a vegetable.")
session.add(broccoli)
session.commit()

carrot = Item(name="Carrot", category=category1, description="A carroy  is a root vegetable, usually orange in color, though purple, red, white, and yellow varieties exist.")
session.add(carrot)
session.commit()

zucchini = Item(name="Zucchini", category=category1, description="Zucchini is a summer squash which can reach nearly a meter in length, but which is usually harvested at half that size or less.")
session.add(zucchini)
session.commit()

celery = Item(name="Celery", category=category1, description="Celery is a cultivated plant, variety in the family Apiaceae, commonly used as a vegetable")
session.add(celery)
session.commit()

bacon = Item(name="Bacon", category=category2, description="meat from a pig that is treated with smoke or salt, and is often cooked in rashers (=thin pieces)")
session.add(bacon)
session.commit()

beef = Item(name="Beef", category=category2, description="Meat from a cow")
session.add(beef)
session.commit()

pork = Item(name="Pork", category=category2, description="Meat from a pig")
session.add(pork)
session.commit()

chicken = Item(name="Chicken", category=category2, description="Meat from a chicken")
session.add(chicken)
session.commit()

bagel = Item(name="Bagel", description="Ring shaped, usually with a dense, chewy interior; usually topped with sesame or poppy seeds baked into the surface.", category=category3)
session.add(bagel)
session.commit()

brioche = Item(name="Brioche", category=category3, description="A highly enriched bread, noted for its high butter and egg content, commonly served as a component of French desserts.")
session.add(brioche)
session.commit()

whitebread = Item(name="White Bread", category=category3, description="Made from wheat flour from which the bran and the germ have been removed through a process known as milling.")
session.add(whitebread)
session.commit()

multigrainbread = Item(name="Multigrain bread", category=category3, description="Bread prepared with two or more types of grain")
session.add(multigrainbread)
session.commit()

milk = Item(name="Milk", category=category4, description="A white liquid produced by the mammary glands of mammals. It is the primary source of nutrition for young mammals before they are able to digest other types of food.")
session.add(milk)
session.commit()

butter = Item(name="Butter", category=category4, description="Butter is a solid dairy product made by churning fresh or fermented cream or milk, to separate the butterfat from the buttermilk.")
session.add(butter)
session.commit()

cottagecheese = Item(name="Cottage cheese", category=category4, description="A cheese curd product with a mild flavor. It is drained, but not pressed, so some whey remains and the individual curds remain loose.")
session.add(cottagecheese)
session.commit()

cream = Item(name="Cream", category=category4, description="Composed of the higher-butterfat layer skimmed from the top of milk before homogenization. In un-homogenized milk, the fat, which is less dense, will eventually rise to the top.")
session.add(cream)
session.commit()

print "added lots of item!"
