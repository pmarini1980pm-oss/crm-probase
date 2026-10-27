import sqlite3, os, time, json
from datetime import datetime, timedelta
from pathlib import Path
MARKER="demo_seed_v1"
BASE=datetime(1899,12,30)
NAMES=['Ana Souza','Bruno Ribeiro','Carla Costa','Daniel Oliveira','Elisa Barros','Fabio Carvalho','Gabriela Moreira','Henrique Almeida','Isabela Ferreira','Joao Rocha','Karina Mendes','Lucas Duarte','Mariana Gomes','Nelson Campos','Olivia Martins','Paulo Lima','Renata Santos','Sergio Pereira','Tatiana Nunes','Vitor Araujo']
CITIES=['Cidade Fictícia A','Cidade Fictícia B','Cidade Fictícia C','Cidade Fictícia D']
SECTORS=['Pintura','Areia e pedra','Outros materiais']
ORIGINS=['WhatsApp','Indicação','Loja física','Cadastro manual','Instagram']
PRODUCTS=[('Tinta acrílica premium 18 L','Pintura','un',289),('Rolo de pintura 23 cm','Pintura','un',39),('Massa corrida 25 kg','Pintura','un',89),('Areia média','Areia e pedra','m³',185),('Pedra britada','Areia e pedra','m³',210),('Cimento 50 kg','Outros materiais','sc',41),('Argamassa 20 kg','Outros materiais','sc',32),('Piso cerâmico','Outros materiais','m²',69)]
STAGES=['Novo contato','Qualificação','Orçamento','Orçamento enviado','Negociação','Venda ganha','Venda perdida','Compra futura']
ACTIONS=['Retornar ao cliente','Conferir medidas','Preparar proposta','Confirmar interesse','Agendar atendimento']
AMOUNTS=[1673.26,235.68,763.62,1594.58,3842.84,932.35,149.58,734.6,7020.02,651.83,780.06,2380.53,2227.06,480.35,183.58,845.53,6612.72,863.7,370.72,3913.8,2836.38,1107.64,170.44,1683.26,6774,1008.32,1250.05,2302.07,1211.12,696.06,686.2,902.34,7282.82,800.39,1810.32,404.03,1500.41,972.54,395.63,774.74,2836.57,1059.74,2077.24,3699.69,3417.57,663.85,693.42,928.09,5770.5,668.15,350.63,1839.33,2981.59,819.86,110.81,820.47,1273.24,355.28,1898.72,4772.77,1574.99,894.1,473.86,1668.14,1023.18,859.04,612.81,3835.35,1496.75,83,448.01,276.76,5433.22,741.09,1924.9,4687.37,2919.07,101.04,229.82,690.04,2320.01,289.11,274.39,4051.73,1610.32]
QTY=[6,14,6,7,6,14,7,7,4,14,16,11,5,2,5,12,7,5,10,4,5,12,15,8,18,7,8,12,11,5,16,17,16,7,16]
def ts(serial): return int((BASE+timedelta(days=float(serial))).timestamp())
def day(serial): return (BASE+timedelta(days=float(serial))).date().isoformat()
def cents(v): return int(round(float(v)*100))
def seed_if_possible(db_path=None):
    db_path=db_path or os.environ.get('CRM_DB') or str(Path(__file__).resolve().parent/'data'/'crm.sqlite3')
    p=Path(db_path)
    if not p.exists(): return False,'db_missing'
    db=sqlite3.connect(str(p),timeout=30); db.execute('PRAGMA foreign_keys=ON')
    try:
        try: user=db.execute('SELECT id FROM users WHERE active=1 ORDER BY id LIMIT 1').fetchone()
        except sqlite3.OperationalError: return False,'schema_missing'
        if not user: return False,'waiting_user'
        if db.execute('SELECT value FROM settings WHERE key=?',(MARKER,)).fetchone(): return True,'already_seeded'
        owner=int(user[0]); clients=[]; opps=[]; db.execute('BEGIN IMMEDIATE')
        for i in range(60):
            suffix='' if i<20 else f' Demo {i//20+1}'; frac=(9-(i%8))/24
            cur=db.execute('INSERT INTO clients(name,phone,email,city,notes,owner_id,sector,source,paused,last_inbound,created) VALUES(?,?,?,?,?,?,?,?,?,?,?)',(NAMES[i%20]+suffix,f'0097{i:07d}',f'cliente.demo{i+1:03d}@example.invalid',CITIES[i%4],'Cliente fictício para treinamento. NÃO CONTATAR.',owner,SECTORS[i%3],ORIGINS[i%5],0,None,ts(46322-i+frac)))
            clients.append(cur.lastrowid)
        for i,amount in enumerate(AMOUNTS):
            prod,sector,unit,price=PRODUCTS[i%8]; stage=STAGES[i%8]
            cur=db.execute('INSERT INTO opportunities(client_id,title,sector,owner_id,stage,amount,priority,next_action,due,notes,loss_reason,created,updated) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)',(clients[i%60],f'Pedido fictício {i+1:03d} - {prod}',sector,owner,stage,cents(amount),['Normal','Alta','Urgente'][i%3],ACTIONS[i%5],day(46313+(i%23)),'DADO FICTÍCIO - uso exclusivo para treinamento','Cliente optou por adiar a compra' if stage=='Venda perdida' else '',ts(46322-(i%35)+.375),ts(46322.375)))
            opps.append(cur.lastrowid)
        titles=['Retornar ligação','Conferir orçamento','Verificar necessidade','Confirmar recebimento']
        for i in range(110):
            oi=i%85; db.execute('INSERT INTO tasks(title,client_id,opportunity_id,owner_id,due,done,kind,dedupe,created) VALUES(?,?,?,?,?,?,?,?,?)',(titles[i%4],clients[oi%60],opps[oi],owner,day(46315+(i%19)),1 if i%5==0 else 0,'automatic' if i%4==0 else 'manual',None,ts(46322-(i%22)+.375)))
        last={}
        for i in range(150):
            cid=clients[i%60]; incoming=i%3!=0; created=ts(46316.125+i/24); body='Olá, gostaria de informações sobre materiais para minha obra. [MENSAGEM FICTÍCIA]' if incoming else 'Atendimento de demonstração: vamos preparar uma proposta. [MENSAGEM FICTÍCIA]'
            db.execute('INSERT INTO messages(client_id,direction,body,status,external_id,request_key,created) VALUES(?,?,?,?,?,?,?)',(cid,'in' if incoming else 'out',body,'received' if incoming else 'simulated',None,None,created))
            if incoming: last[cid]=max(created,last.get(cid,0))
        for cid,created in last.items(): db.execute('UPDATE clients SET last_inbound=? WHERE id=?',(created,cid))
        for i,q in enumerate(QTY):
            prod,sector,unit,price=PRODUCTS[i%8]; total=q*price; item=[{'description':prod,'quantity':float(q),'unit':unit,'sale_price':cents(price),'total':cents(total)}]
            db.execute('INSERT INTO quotes(opportunity_id,version,items,total,valid_until,status,created_by,created) VALUES(?,?,?,?,?,?,?,?)',(opps[i],1,json.dumps(item,ensure_ascii=False),cents(total),day(46342+(i%10)),'draft',owner,int(time.time())))
        db.execute('INSERT OR REPLACE INTO settings(key,value) VALUES(?,?)',(MARKER,'true')); db.commit(); return True,'seeded 60 clients, 85 opportunities, 110 tasks, 150 messages, 35 quotes'
    except Exception:
        db.rollback(); raise
    finally: db.close()
