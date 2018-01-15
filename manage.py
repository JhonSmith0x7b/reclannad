#-*- coding:utf-8 -*-
from app import app 


@app.cli.command()
def test():
    """
    test cli command
    """
    from app.main import logic
    ll = logic.LoginLogic()    
    ll.signup('1', '2')









if __name__ == '__main__':
    app.run()