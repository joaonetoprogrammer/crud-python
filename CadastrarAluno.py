from tkinter import*
from tkinter import ttk
from PIL import ImageTk, Image
import django
import datetime
import MySQLdb
from tkinter import messagebox



class userwindow:
    mysqlVar = 0
    cursorVar = 0
    itemVar = 0

    def refresh(self):
        self.update_tree()
        self.clean_entries()

    def search_record(self):
        try:
            self.tree.delete(*self.tree.get_children())
            self.cursorVar.execute("SELECT * FROM estudante WHERE Nome like %s or Telefone like %s",('%'+self.search_value.get()+'%','%'+self.search_value.get()+'%' ))
            self.result = self.cursorVar.fetchall()
            length = str(len(self.result))

            if(length==0):
                messagebox.showinfo("SISTEMA DE ALUNOS", "NÃO FOI POSSÍVEL ENCONTRAR NENHUM CADASTRO COM ESSE VALOR")
            if(length!='0'):
                i=0
                for row in self.result:
                    if(i%2==0):
                        self.tree.insert("", END, values=row,tag='1')
                    else:
                        self.tree.insert("", END, values=row,tag='2')
                    i = i+1
        except:
            raise
            messagebox.showerror("SISTEMA DE ALUNOS", "NÃO FOI POSSÍVEL FAZER UMA CONEXÃO DE DADOS")

    def clean_entries(self):
        self.search_value.set("")


    def update_tree(self):
        try:
            self.tree.delete(*self.tree.get_children())
            self.cursorVar.execute("SELECT * FROM estudante")
            self.rows = self.cursorVar.fetchall()
    
            i= 0
            for row in self.rows:
                if(i%2==0):
                    self.tree.insert("", END, values=row,tag='1')
                else:
                    self.tree.insert("", END, values=row,tag='2')
                i=i+1
        
        except:
            messagebox.showerror("SISTEMA DE ALUNOS", "NÃO FOI POSSÍVEL ATUALIZAR DADOS")
    
    def conexaoBD(self):
        try:

            self.mysqlVar = MySQLdb.connect(host="localhost",    # seu host
                                            user="root",      # seu user
                                            passwd="tijk#@56#jn090@tim",      # sua senha
                                            db="sistemaalunos")          # nome do seu banco de dados
            self.cursorVar = self.mysqlVar.cursor()
        except:
            messagebox.showerror("SISTEMA DE ALUNOS", "NÃO FOI POSSÍVEL CONECTAR COM O BANCO DE DADOS. REINICIE O SISTEMA OU ENTRE EM CONTATO COM O PROGRAMADOR DO SISTEMA")

        finally:
            self.mysqlVar.commit()
            self.update_tree()

    def __init__(self):
        
        self.user_window = Tk()
        self.user_window.resizable(False, False)
        self.user_window.title("Cadastro de Usuários")
        self.user_window.iconbitmap("logoLogin.ico")

        
        self.tree = ttk.Treeview(self.user_window, selectmode ="browse", column= ("column1", "column2", "column3","column4"), show='headings')
        self.tree.column("column1", width=100, minwidth=100,stretch=NO)
        self.tree.heading("#1", text="Acesso: ")
        self.tree.column("column2", width=180, minwidth=180,stretch=NO)
        self.tree.heading("#2", text="Nome: ")
        self.tree.column("column3", width=180, minwidth=180,stretch=NO)
        self.tree.heading("#3", text="Telefone: ")
        self.tree.column("column4", width=480, minwidth=480,stretch=NO)
        self.tree.heading("#4", text="Endereço:")
        self.tree.tag_configure('1', background='ivory2')
        self.tree.tag_configure('2', background='ivory2')


        self.tree.grid(row=4, column=0, columnspan=4, padx=9, pady=9, sticky=W+E)

        Label(self.user_window, text="Pesquisar por nome ou por telefone: ").grid(row=5,column=0,columnspan=2, sticky=E, padx=9, pady=9)
        self.search_value = StringVar(self.user_window, value="")
        Entry(self.user_window, textvariable=self.search_value).grid(row=5, column=2, padx=10, pady=10, sticky=W+E)

        self.botaoSearch = ttk.Button(self.user_window, text="Pesquisar", command = self.search_record)
        self.botaoSearch.grid(row=5, column=3, padx=9, sticky=W+E)

        self.botaoAtualizarBD = ttk.Button(self.user_window, text="Atualizar", command=self.refresh)
        self.botaoAtualizarBD.grid(row=6, column=2, padx=9, sticky=W+E)

        self.conexaoBD()
        self.user_window.mainloop()
        
        
class adminwindow:
    mysqlVar = 0
    cursorVar = 0
    itemVar = 0

    def refresh(self):
        self.update_tree()
        self.clean_entries()
        #print("Atualizar")

    def seach_record(self):
        try:
            self.tree.delete(*self.tree.get_children())
            self.cursorVar.execute("SELECT * FROM estudante where Nome like %s or Telefone like %s",('%'+self.searchvalue.get()+'%','%'+self.searchvalue.get()+'%' ))
            self.result = self.cursorVar.fetchall()
            length = str(len(self.result))

            if(length==0):
                messagebox.showinfo("SISTEMA DE ALUNOS", "NÃO FOI POSSÍVEL ENCONTRAR NENHUM CADASTRO COM ESSE VALOR")
            if(length!='0'):
                i=0
                for row in self.result:
                    if(i%2==0):
                        self.tree.insert("", END, values=row,tag='1')
                    else:
                        self.tree.insert("", END, values=row,tag='2')
                    i = i+1
        except:
            raise
            messagebox.showerror("SISTEMA DE ALUNOS", "NÃO FOI POSSÍVEL FAZER UMA CONEXÃO DE DADOS")

    def reset_db(self):
        yesno=messagebox.askquestion("SISTEMA DE ALUNOS","DESEJA REALMENTE DELETAR TODOS OS DADOS DO BANCO DE DADOS?")
        if (yesno=='yes'):
            self.cursorVar.execute("DROP TABLE estudante")
            messagebox.showinfo("SISTEMA DE ALUNOS", "TODOS OS DADOS DO BANCO DE DADOS FORAM DELETADOS")
            self.conexaoBD()
            self.update_tree()

    def clean_entries(self):
        self.campoEndereco.delete(0, "end")
        self.campoNome.delete(0, "end")
        self.campoTelefone.delete(0, "end")

    def delete_record(self):
        try:
            self.cursorVar.execute("delete FROM estudante WHERE ID=%s", (self.itemVar['values'][0],))
            messagebox.showinfo("SISTEMA DE ALUNOS","DADOS DELETADOS")
        except:
            messagebox.showerror("SITEMA DE ALUNOS","NÃO FOI POSSÍVEL DELETAR ESSES DADOS")
        finally:
            self.itemVar=0
            self.clean_entries()
            self.update_tree()
            self.mysqlVar.commit()

    def update_record(self):
        if(self.Name_value.get()!="" and self.Andress_value.get()!="" and self.Phone_no_value.get()!=""):
            try:
                self.cursorVar.execute("""UPDATE estudante SET Nome = %s, Telefone = %s, Endereco = %s WHERE ID = %s""",(self.Name_value.get(), self.Phone_no_value.get(), self.Andress_value.get(), self.itemVar['values'][0]))
                messagebox.showinfo("SISTEMA DE ALUNOS","ATUALIZADO COM SUCESSO")
            except MySQLdb.IntegrityError:
                messagebox.showerror("SISTEMA DE ALUNOS","ESTE ESTUDADNTE JÁ SE ENCONTRA NO BANCO DE DADOS")
            except:
                messagebox.showerror("SISTEMA DE ALUNOS","NÃO FOI POSSÍVEL ATUALIZAR OS DADOS!")
            finally:
                self.update_tree()
                self.mysqlVar.commit()
        else:
                messagebox.showwarning("SISTEMA DE ALUNOS","POR FAVOR PREENCHER TODOS OS CAMPOS")

    def selectItem(self, event):
        self.itemVar = self.tree.item(self.tree.focus())
        #messagebox.showinfo("Cadastro de Alunos", "",self.itemVar)
        self.Name_value.set(self.itemVar["values"][1])
        self.Phone_no_value.set(self.itemVar["values"][2])
        self.Andress_value.set(self.itemVar["values"][3])


    def update_tree(self):
        try:
            self.tree.delete(*self.tree.get_children())
            self.cursorVar.execute("SELECT * FROM estudante")
            self.rows = self.cursorVar.fetchall()
    
            i= 0
            for row in self.rows:
                if(i%2==0):
                    self.tree.insert("", END, values=row,tag='1')
                else:
                    self.tree.insert("", END, values=row,tag='2')
                i=i+1
        
        except:
            messagebox.showerror("SISTEMA DE ALUNOS", "NÃO FOI POSSÍVEL ATUALIZAR DADOS")
    
    def write_record(self):
        if(self.Name_value.get()!="" and self.Andress_value.get()!="" and self.Phone_no_value.get()!=""):
            try:
                self.cursorVar.execute("INSERT INTO estudante (Nome, Telefone, Endereco) VALUES (%s,%s,%s)",(self.Name_value.get(), self.Phone_no_value.get(), self.Andress_value.get()))
                self.mysqlVar.commit()
                """
                self.cursorVar.execute("SELECT * max(ID) FROM estudante")
                self.rows = self.cursorVar.fetchall()
                messagebox.showinfo("SISTEMA DE ALUNOS",""+self.rows[0][0]+"{Nome : "+self.rows[0][1]+"| No : "+self.rows[0][2]+"| Endereco : "+self.rows[0][3],"} FOI CADASTRADO !")
                """
                messagebox.showinfo("SISTEMA DE ALUNOS", "CADASTRO REALIZADO COM SUCESSO")
                self.clean_entries()
        

            except MySQLdb.IntegrityError:
                messagebox.showerror("SISTEMA DE ALUNOS","ESTE ESTUDADNTE JÁ SE ENCONTRA NO BANCO DE DADOS")
        
            finally:
                self.update_tree()
        
        else:
            messagebox.showwarning("SISTEMA DE ALUNOS", "POR FAVOR PREENCHA TODOS OS CAMPOS")
    def conexaoBD(self):
        try:

            self.mysqlVar = MySQLdb.connect(host="localhost",    # seu host
                                            user="root",      # seu user
                                            passwd="tijk#@56#jn090@tim",      # sua senha
                                            db="sistemaalunos")          # nome do seu banco de dados
            self.cursorVar = self.mysqlVar.cursor()
        except:
            messagebox.showerror("SISTEMA DE ALUNOS", "NÃO FOI POSSÍVEL CONECTAR COM O BANCO DE DADOS. REINICIE O SISTEMA OU ENTRE EM CONTATO COM O PROGRAMADOR DO SISTEMA")

        finally:
            self.mysqlVar.commit()
            self.update_tree()
    def __init__(self):
            
        self.admin_window = Tk()
        self.admin_window.resizable(False, False)
        self.admin_window.title("ADMINISTRADOR")
        self.admin_window.iconbitmap("logoLogin.ico")
       
        self.nome = Label(self.admin_window, text="Nome: ")
        self.nome.grid(row=0,column=0, sticky=W, padx=10, pady=10)
               
        self.telefone = Label(self.admin_window, text="Telefone: ")
        self.telefone.grid(row=1,column=0, sticky=W, padx=10, pady=10)

        self.endereco = Label(self.admin_window, text="Endereço: ")
        self.endereco.grid(row=2,column=0, sticky=W, padx=10, pady=10)

        self.Name_value = StringVar(self.admin_window, value="")
        self.campoNome = ttk.Entry(self.admin_window, textvariable=self.Name_value)
        self.campoNome.grid(row=0, column=1, columnspan=2, padx=10, pady=10, sticky=W+E)

        self.Phone_no_value = StringVar(self.admin_window, value="")
        self.campoTelefone = ttk.Entry(self.admin_window, textvariable=self.Phone_no_value)
        self.campoTelefone.grid(row=1, column=1, columnspan=2, padx=10, pady=10, sticky=W+E)

        self.Andress_value = StringVar(self.admin_window, value="")
        self.campoEndereco = ttk.Entry(self.admin_window, textvariable=self.Andress_value)
        self.campoEndereco.grid(row=2, column=1, columnspan=2, padx=10, pady=10, sticky=W+E)

        self.botaoCadastrar = ttk.Button(self.admin_window, text="Cadastrar", command = self.write_record)
        self.botaoCadastrar.grid(row=0, column=3, padx=9, sticky=W+E)

        self.botaoAtualizar = ttk.Button(self.admin_window, text="Atualizar", command = self.update_record)
        self.botaoAtualizar.grid(row=1, column=3, padx=9, sticky=W+E)

        self.botaoDeletar = ttk.Button(self.admin_window, text="Deletar", command = self.delete_record)
        self.botaoDeletar.grid(row=2, column=3, padx=9, sticky=W+E)

        self.tree = ttk.Treeview(self.admin_window, selectmode ="browse", column= ("column1", "column2", "column3","column4"), show='headings')
        self.tree.column("column1", width=100, minwidth=100,stretch=NO)
        self.tree.heading("#1", text="Acesso: ")
        self.tree.column("column2", width=180, minwidth=180,stretch=NO)
        self.tree.heading("#2", text="Nome: ")
        self.tree.column("column3", width=180, minwidth=180,stretch=NO)
        self.tree.heading("#3", text="Telefone: ")
        self.tree.column("column4", width=480, minwidth=480,stretch=NO)
        self.tree.heading("#4", text="Endereço:")
        
        self.tree.bind("<ButtonRelease-1>", self.selectItem)
        self.tree.bind("<space>", self.selectItem)
        self.tree.tag_configure('1', background='ivory2')
        self.tree.tag_configure('2', background='ivory2')

        self.tree.grid(row=4, column=0, columnspan=4, padx=9, pady=9, sticky=W+E)
        
        Label(self.admin_window, text="Pesquisar por nome ou por telefone: ").grid(row=5,column=0,columnspan=2, sticky=E, padx=9, pady=9)

        self.searchvalue = StringVar(self.admin_window, value="")
        Entry(self.admin_window, textvariable=self.searchvalue).grid(row=5, column=2, padx=10, pady=10, sticky=W+E)

        self.botaoSearch = ttk.Button(self.admin_window, text="Pesquisar", command=self.seach_record)
        self.botaoSearch.grid(row=5, column=3, padx=9, sticky=W+E)

        self.botaoLimpar = ttk.Button(self.admin_window, text="Limpar Banco de Dados", command=self.reset_db)
        self.botaoLimpar.grid(row=6, column=3,pady=10,padx=9, sticky=W+E)
        
        self.botaoAtualizarBD = ttk.Button(self.admin_window, text="Atualizar", command= self.refresh)
        self.botaoAtualizarBD.grid(row=6, column=2, padx=9, sticky=W+E)

        self.conexaoBD()
        self.admin_window.mainloop()





class signinwindow:
    mysqlVar = 0
    cursorVar = 0
    itemVar = 0

    def conexaoBD(self):
        try:

            self.mysqlVar = MySQLdb.connect(host="localhost",    # seu host
                                            user="root",      # seu user
                                            passwd="tijk#@56#jn090@tim",      # sua senha
                                            db="sistemaalunos")          # nome do seu banco de dados
            self.cursorVar = self.mysqlVar.cursor()
        except:
            messagebox.showerror("SISTEMA DE ALUNOS", "NÃO FOI POSSÍVEL CONECTAR COM O BANCO DE DADOS. REINICIE O SISTEMA OU ENTRE EM CONTATO COM O PROGRAMADOR DO SISTEMA")

        finally:
            self.mysqlVar.commit()

    def user_tree_update(self):
        self.tree.delete(*self.tree.get_children())
        self.cursorVar.execute("SELECT * FROM users")
        res = self.cursorVar.fetchall()
        i = 0
        for row in res:
            if(i%2==0):
                self.tree.insert("", END, values=row,tag='1')
            else:
                self.tree.insert("", END, values=row,tag='2')
            i = i +1
    

    def clear_users(self):
        self.cursorVar.execute("TRUNCATE TABLE users")
        self.conexaoBD()
        self.user_tree_update()


    def view_users(self):
        try:
            self.cursorVar.execute("SELECT * from users")
            res = self.cursorVar.fetchall()
        except:
            messagebox.showerror("SISTEMA DE ALUNOS", "NÃO FOI POSSÍVEL CARREGAR O BANCO DE DADOS. REINICIE O SISTEMA OU ENTRE EM CONTATO COM O PROGRAMADOR DO SISTEMA")


        self.x = Tk()
        self.x.resizable(False, False)
        self.x.title("Lista de Usuários")
        self.x.iconbitmap("logoLogin.ico")

        
        self.tree = ttk.Treeview(self.x, selectmode ="browse", column= ("column1", "column2"), show='headings')
        self.tree.heading("#1", text="Usuário")
        self.tree.heading("#2", text="Senhas")
        self.tree.tag_configure('1', background='yellow')
        self.tree.tag_configure('2', background='light green')

        self.tree.grid(row=0, column=0, columnspan=4, padx=9, pady=9, sticky=W+E)

        Button(self.x,text="Limpar Usuários", command=self.clear_users).grid(row=1, column=0, columnspan=4, padx=9, pady=9, sticky=W+E)
       
        self.user_tree_update()
        self.x.mainloop()

    def new_user(self):
        try:
            if (self.username_text.get()!="" and self.password_text.get()!=""):
                self.cursorVar.execute("INSERT INTO users (usuario,senha) VALUES (%s,%s)",(self.username_text.get(),self.password_text.get()))
                self.signin_window.destroy()
                messagebox.showinfo("SISTEMA DE ALUNOS", "CADASTRO REALIZADO COM SUCESSO")
            else:
                messagebox.showwarning("SISTEMA DE ALUNOS", "POR FAVOR PREENCHER TODOS OS CAMPOS")
        
        except MySQLdb.IntegrityError:
            messagebox.showerror("SISTEMA DE ALUNOS", "ESSE USUÁRIO JÁ SE ENCONTRA NO BANCO DE DAODS")
        
        except:
            messagebox.showerror("SISTEMA DE ALUNOS", "NÃO FOI POSSÍVEL CADASTRAR OS DADOS")
        
        finally:
            self.mysqlVar.commit()
            self.cursorVar.execute("SELECT * from users")
            res=self.cursorVar.fetchall()
            self.username_text.set("")
            self.password_text.set("")



    def __init__(self):
            
        self.signin_window = Toplevel()
        self.signin_window.resizable(False, False)
        self.signin_window.title("CADASTRAR LOGIN")
        self.signin_window.iconbitmap("logoLogin.ico")
       
        self.username_text = StringVar()
        self.password_text = StringVar()

        Label(self.signin_window, text="Cadastrar Login", font ="Times, 20",foreground="black").grid(row=0,column=0, columnspan= 19, padx=10, pady=5)
        Label(self.signin_window, text="Usuário: ", font ="Times, 16",foreground="black").grid(row=1,column=0,pady=5,padx=10)
        Label(self.signin_window, text="Senha: ", font ="Times, 16",foreground="black").grid(row=2,column=0,pady=5,padx=10)
        # sticky w = alinhado a esquerda
        # sticky e = alinhado a direita
        # sticky m
        # sticky n

        Entry(self.signin_window, font="Times,10", textvariable=self.username_text).grid(row=1, column=1, sticky= W, padx= 10)
        Entry(self.signin_window, font="Times,10", textvariable=self.password_text).grid(row=2, column=1, sticky =W, padx = 10)

        butViewUsers = Button(self.signin_window, text='Visualizar Cadastros', command=self.view_users)
        butViewUsers.configure(width=24,height=2)
        butViewUsers.grid(row=3,column =1,padx=11, sticky =W, pady=10)

        butcadastrarusuario = Button(self.signin_window, text='Cadastrar', command=self.new_user)
        butcadastrarusuario.configure(width=10,height=2,foreground='white',background='orange')
        butcadastrarusuario.grid(row=3, sticky =W, padx=18, pady=10)

        self.conexaoBD()
        self.signin_window.mainloop()

# CLASSE LOGIN
class loginwindow():
    mysqlVar = 0
    cursorVar = 0
    itemVar = 0
    
    def conexaoBD(self):
        try:

            self.mysqlVar = MySQLdb.connect(host="localhost",    # seu host
                                            user="root",      # seu user
                                            passwd="tijk#@56#jn090@tim",      # sua senha
                                            db="sistemaalunos")          # nome do seu banco de dados
            self.cursorVar = self.mysqlVar.cursor()
        except:
            messagebox.showerror("SISTEMA DE ALUNOS", "NÃO FOI POSSÍVEL CONECTAR COM O BANCO DE DADOS. REINICIE O SISTEMA OU ENTRE EM CONTATO COM O PROGRAMADOR DO SISTEMA")

        finally:
            self.mysqlVar.commit()
    
    def logg(self):
        try:
            self.cursorVar.execute("SELECT * FROM users")
            res=self.cursorVar.fetchall()
            flag=0
            for x in res:
                if(self.var.get()==1 and self.username_text.get()==x[0] and self.password_text.get()==x[1]):
                    self.login_window.destroy()
                    userwindow()
                    flag=1
            if(self.var.get()==2 and self.username_text.get()=="JoaoNeto" and self.password_text.get()=="timao89835019"):
                self.login_window.destroy()
                adminwindow()
                flag=1
            if(flag==0):
                messagebox.showwarning("SISTEMA DE ALUNOS", "POR FAVOR PREENCHER TODOS OS CAMPOS")
        
        except:
            messagebox.showerror("SISTEMA DE ALUNOS", "OCORREU UM ERRO AO ENTRAR")
            raise
        finally:
            self.password_text.set("")
            self.username_text.set("")
        

    def __init__(self):
            
        self.login_window = Toplevel()
        self.login_window.resizable(False, False)
        self.login_window.title("LOGIN")
        self.login_window.iconbitmap("logoLogin.ico")

        self.username_text = StringVar(self.login_window)
        self.password_text = StringVar(self.login_window)
        self.var= IntVar(self.login_window)

        Label(self.login_window, text="Login", font ="Times, 20",foreground="black").grid(row=0,column=0, columnspan= 19, padx=10, pady=5)
        Label(self.login_window, text="Usuário: ", font ="Times, 16",foreground="black").grid(row=1,column=0,pady=5,padx=10)
        Label(self.login_window, text="Senha: ", font ="Times, 16",foreground="black").grid(row=2,column=0,pady=5,padx=10)

        self.username = Entry(self.login_window, font="Times,10", textvariable=self.username_text).grid(row=1,column=1, padx=10)
        self.usersenha = Entry(self.login_window, font="Times,10",textvariable=self.password_text, show="*").grid(row=2,column=1,padx=10)

        self.but = Button(self.login_window, text='Entrar', command=self.logg)
        self.but.configure(width=9, height=1, foreground='white',background='orange')
        self.but.grid(row=3,columnspan= 3, sticky=E,pady=10,padx=13)

        self.var.set(1)

        Radiobutton(self.login_window,text="Usuário",variable=self.var, value=1).grid(row=3, sticky=W,padx=14)
        Radiobutton(self.login_window,text="Administrador",variable= self.var,value=2).grid(row=3, columnspan=2,padx=5)
        
        self.conexaoBD()

        self.login_window.mainloop()

# CLASSE DA TELA INICIAL
class mainwindow():
    def funcao_botaoAjuda(self):
        import os, webbrowser
        from urllib.request import pathname2url
        url = 'file:{}'.format(pathname2url(os.path.abspath('help.html')))
        webbrowser.open(url)


    def funcao_botaoSobre(self):
        messagebox.showinfo("SITEMA DE CADASTRO DE ALUNOS", "ESSE SISTEMA FOI DESENVOLVIDO PARA ORGANIZAÇÃO DE CADASTRO DE ALUNOS\n"
        "ELE FOI PROGRAMADO POR JOAO NETO\n\nCONTATOS:\nINSTAGRAM: @JOAONETOEMP\nEMAIL: joaonetoempreendedor@gmail.com\nTWITTER: @JOAONETOEMP")
    
    def funcao_botaoEntrar(self):
        try:
            signinwindow()
        except:
            raise Exception("ERRO NO SISTEMA -\n REINICIE OU CONSULTE O PROGRAMADOR DO SISTEMA")

    def funcao_botaologar(self):
        try:
            loginwindow()
        except:
            raise Exception("ERRO NO SISTEMA -\n REINICIE OU CONSULTE O PROGRAMADOR DO SISTEMA")

    def funcao_botaosair(self):
        if messagebox.askokcancel("Sitema de Alunos", "Deseja realmente sair?"):
            self.root.destroy()

   

    def __init__(self):
        self.root = Tk()
        self.root.resizable(False, False)
        self.root.protocol("WM_DELETE_WINDOW",self.funcao_botaosair)
        self.root.title("LOGIN - SISTEMA DE ALUNOS")
        self.img = ImageTk.PhotoImage(Image.open("login.png"))
        self.panel = Label(self.root, image = self.img)
        self.panel.grid(row=0, column = 1,padx=10)
        self.root.iconbitmap("logoLogin.ico")
        
        Label(self.root, text="Sistema de Cadastro\n de Aluno", font ="Times, 20",foreground="black").grid(row=0,column=0,pady=5,padx=10)
        
        self.but = Button(self.root, text='Login', command=self.funcao_botaologar)
        self.but.configure(width=18, height=2, foreground='white',background='orange')
        self.but.grid(row=1,columnspan=2, sticky=N,pady=25)
        
        self.menu_bar = Menu(self.root)
        self.menu_bar.add_separator()

        self.file_menu = Menu(self.menu_bar, tearoff = 0)
        self.file_menu.add_command(label="Entrar", command=self.funcao_botaoEntrar)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Sair", command=self.funcao_botaosair)
        self.menu_bar.add_cascade(label="File", menu = self.file_menu)
        self.menu_bar.add_separator()
    
        
        self.help_menu = Menu(self.menu_bar, tearoff = 0)
        self.help_menu.add_command(label="Ajuda", command=self.funcao_botaoAjuda)
        self.help_menu.add_separator()
        self.help_menu.add_command(label="Sobre", command=self.funcao_botaoSobre)
        self.menu_bar.add_cascade(label="Ajuda", menu = self.help_menu)

        self.root.configure(menu = self.menu_bar)
        self.root.mainloop()



        self.root.mainloop()

try:
    mainwindow()

except:
    raise Exception("NÃO PODE SER CRIADO ESSE FORMULÁRIO")
