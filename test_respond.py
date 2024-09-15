from app import respond

def test_respond():
    test = respond('Hello!',[],'You only respond hello.',5,1,1.5,False)
    
    with open('log.txt','w') as f:
        f.write(f'{type(test)}\n')

    assert type(test) == dict
