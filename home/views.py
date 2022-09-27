
from django.shortcuts import render, HttpResponse
import mysql.connector as sql

no=''
dia=''
n=''
fr=''
fa=''
ka=''
lyf=''
ansvs={}
xyval=''

# Create your views here.
def index(request):
    return render(request, 'homedms.html')

def dgbbip(request):
    global no,dia,n,fr,fa,ka,lyf,ansvs
    if request.method=='POST':
        zdb=sql.connect(host="localhost",user="root",passwd="Aryan29425",database='dgbb')
        cursor=zdb.cursor()
        aget=request.POST
        for key,value in aget.items():
            if key=="dia":
                dia=value
            if key=="rpm":
                n=value
            if key=="rload":
                fr=value
            if key=="aload":
                fa=value
            if key=="lfactor":
                ka=value
            if key=="elife":
                lyf=value
        
        adb="select no from dgbbip1 ORDER BY no DESC LIMIT 1;"
        cursor.execute(adb)
        bget=cursor.fetchall()
        j=0
        kno=0
        
        for bgetEle in bget:
            j=bgetEle[0]
    
        kno=j+1
        bdb="insert into dgbbip1 Values('{}','{}','{}','{}','{}','{}','{}')".format(kno,dia,n,fr,fa,ka,lyf)
        cursor.execute(bdb)
        zdb.commit()
        
        cdb="SELECT * FROM dgbb.series60 where d >= (SELECT dia FROM dgbbip1 ORDER BY no DESC LIMIT 1);"
        cursor.execute(cdb)
        cget=cursor.fetchone()
        #print(cget)
        staticC=cget[8]
        dynamicC=cget[9]
        #print(staticC)
        #print(dynamicC)
        dget=cursor.fetchall()
        faByStaticC=round(int(fa) / staticC,3)
        #print(faByStaticC)
        faByFr=round( int(fa) / int(fr),3)
        #print(faByFr)
        faco = (faByStaticC,)
        ddb="SELECT * FROM dgbb.eqbrgload WHERE faco >= '%f'" % faco
        cursor.execute(ddb)
        dget=cursor.fetchone()
        
        e=dget[1]
        #print(e)
        

        if faByFr > e:
            xyval=' Fa/Fr is greater than e'
            #print("inside if")
            gx=dget[4]
            gy=dget[5]
            #print(e,gx,gy)
        else:
            xyval=' Fa/Fr is less or equal to e'
            gx=dget[2]
            gy=dget[3]
        pe=round((gx* int(fr)+ gy* int(fa))* float(ka),2)
            #print(pe)
        mlRevL10=(int(lyf)*60* int(n)) / 1000000
        #print(mlRevL10)

        dynamicC2=round(round(mlRevL10 ** (1. / 3),2) * pe,2)
        #print(dynamicC2)
        if dynamicC2 <= dynamicC:
            ansvs={
                'op': 'YOUR BEARING OF BASIC DESIGN NO: (SKF)',
                            'skfr': 'SKF',
                            'skf': cget[0],
                            'dr': 'd (mm)',
                            'd': cget[1],
                            'd1r': 'D1 Min. (mm)',
                            'D1': cget[2],
                            'drr': 'D (mm)',
                            'D': cget[3],
                            'd2r': 'D2 Min. (mm)',
                            'D2': cget[4],
                            'br': 'B (mm)',
                            'B': cget[5],
                            'rr': 'r (mm)',
                            'r': cget[6],
                            'r1r': 'r1 (mm)',
                            'r1': cget[7],
                            'cor': 'Static Co (N)',
                            'co': cget[8],
                            'cr':'Dynamic C (N)',
                            'c': cget[9],
                            'spr': 'Max. Speed (rpm)',
                            'sp': cget[10],
                            't1':'Selection od radial and thrust factors:',
                            'fbc': 'Fa/Co',
                            'fbca': faByStaticC ,
                            'fafr': 'Fa/Fr   taking V=1',
                            'fafra': faByFr ,
                            'echk': xyval,
                            'xx': 'X',
                            'xxa': gx,
                            'yy': 'Y',
                            'yya': gy,
                            't2': 'Equivalent Dynamic Load:',
                            'pes': 'Pe in N',
                            'pea': pe,
                            't3': 'Using load life relationship,',
                            'l10': 'L10 in mRev',
                            'l10a': mlRevL10 ,
                            'cd': 'Dynamic C in N',
                            'cda': dynamicC2 ,
                            'cal': 'Calculation:',

                            
                            
            }
            
        else:
        
            #print("inside if check22222222")
            dget=cursor.fetchall()
            cdb="SELECT * FROM series62 where d >= (SELECT dia FROM dgbbip1 ORDER BY no DESC LIMIT 1);"
            
            cursor.execute(cdb)
            cget=cursor.fetchone()
            #print("after cget")
            #print(cget)
            staticC=cget[8]
            dynamicC=cget[9]
            #print(staticC)
            #print(dynamicC)
            dget=cursor.fetchall()
            faByStaticC=round(int(fa) / staticC,3)
            #print(faByStaticC)
            faByFr=round( int(fa) / int(fr),3)
            #print(faByFr)
            faco = (faByStaticC,)
            ddb="SELECT * FROM dgbb.eqbrgload WHERE faco >= '%f'" % faco
            cursor.execute(ddb)
            dget=cursor.fetchone()
            
            e=dget[1]
            #print(e)

            if faByFr > e:
                xyval=' Fa/Fr is greater than e'
                #print("inside if")
                gx=dget[4]
                gy=dget[5]
                #print(e,gx,gy)
            else:
                xyval=' Fa/Fr is less or equal to e'
                gx=dget[2]
                gy=dget[3]
            pe=round((gx* int(fr)+ gy* int(fa))* float(ka),2)
                #print(pe)
            mlRevL10=(int(lyf)*60* int(n)) / 1000000
            #print(mlRevL10)

            dynamicC2=round(round(mlRevL10 ** (1. / 3),2) * pe,2)
            #print(dynamicC2)

            if dynamicC2 <= dynamicC:
                ansvs={
                    'op': 'YOUR BEARING OF BASIC DESIGN NO: (SKF)',
                            'skfr': 'SKF',
                            'skf': cget[0],
                            'dr': 'd (mm)',
                            'd': cget[1],
                            'd1r': 'D1 Min. (mm)',
                            'D1': cget[2],
                            'drr': 'D (mm)',
                            'D': cget[3],
                            'd2r': 'D2 Min. (mm)',
                            'D2': cget[4],
                            'br': 'B (mm)',
                            'B': cget[5],
                            'rr': 'r (mm)',
                            'r': cget[6],
                            'r1r': 'r1 (mm)',
                            'r1': cget[7],
                            'cor': 'Static Co (N)',
                            'co': cget[8],
                            'cr':'Dynamic C (N)',
                            'c': cget[9],
                            'spr': 'Max. Speed (rpm)',
                            'sp': cget[10],
                            't1':'Selection od radial and thrust factors:',
                            'fbc': 'Fa/Co',
                            'fbca': faByStaticC ,
                            'fafr': 'Fa/Fr   taking V=1',
                            'fafra': faByFr ,
                            'echk': xyval,
                            'xx': 'X',
                            'xxa': gx,
                            'yy': 'Y',
                            'yya': gy,
                            't2': 'Equivalent Dynamic Load:',
                            'pes': 'Pe (N)',
                            'pea': pe,
                            't3': 'Using load life relationship,',
                            'l10': 'L10 (mRev)',
                            'l10a': mlRevL10 ,
                            'cd': 'Dynamic C (N)',
                            'cda': dynamicC2 ,
                            'cal': 'Calculation:',
                }
            
            else:
                print("inside if chck 3333333333333")
                dget=cursor.fetchall()
                cdb="SELECT * FROM series63 where d >= (SELECT dia FROM dgbbip1 ORDER BY no DESC LIMIT 1);"
                
                cursor.execute(cdb)
                cget=cursor.fetchone()
                #print("after cget")
                print(cget)
                staticC=cget[8]
                dynamicC=cget[9]
                print(staticC)
                print(dynamicC)
                dget=cursor.fetchall()
                faByStaticC=round(int(fa) / staticC,3)
                print(faByStaticC)
                faByFr=round( int(fa) / int(fr),3)
                print(faByFr)
                faco = (faByStaticC,)
                ddb="SELECT * FROM dgbb.eqbrgload WHERE faco >= '%f'" % faco
                cursor.execute(ddb)
                dget=cursor.fetchone()
                
                e=dget[1]
                print(e)

                if faByFr > e:
                    xyval=' Fa/Fr is greater than e'
                    #print("inside if")
                    gx=dget[4]
                    gy=dget[5]
                    #print(e,gx,gy)
                else:
                    xyval=' Fa/Fr is less or equal to e'
                    gx=dget[2]
                    gy=dget[3]
                pe=round((gx* int(fr)+ gy* int(fa))* float(ka),2)
                print(pe)
                mlRevL10=(int(lyf)*60* int(n)) / 1000000
                print(mlRevL10)

                dynamicC2=round(round(mlRevL10 ** (1. / 3),2) * pe,2)
                print(dynamicC2)
                print(dynamicC)
                if dynamicC2 <= dynamicC:
                    ansvs={
                        'op': 'YOUR BEARING OF BASIC DESIGN NO: (SKF)',
                            'skfr': 'SKF',
                            'skf': cget[0],
                            'dr': 'd (mm)',
                            'd': cget[1],
                            'd1r': 'D1 Min. (mm)',
                            'D1': cget[2],
                            'drr': 'D (mm)',
                            'D': cget[3],
                            'd2r': 'D2 Min. (mm)',
                            'D2': cget[4],
                            'br': 'B (mm)',
                            'B': cget[5],
                            'rr': 'r (mm)',
                            'r': cget[6],
                            'r1r': 'r1 (mm)',
                            'r1': cget[7],
                            'cor': 'Static Co (N)',
                            'co': cget[8],
                            'cr':'Dynamic C (N)',
                            'c': cget[9],
                            'spr': 'Max. Speed (rpm)',
                            'sp': cget[10],
                            't1':'Selection od radial and thrust factors:',
                            'fbc': 'Fa/Co',
                            'fbca': faByStaticC ,
                            'fafr': 'Fa/Fr   taking V=1',
                            'fafra': faByFr ,
                            'echk': xyval,
                            'xx': 'X',
                            'xxa': gx,
                            'yy': 'Y',
                            'yya': gy,
                            't2': 'Equivalent Dynamic Load:',
                            'pes': 'Pe (N)',
                            'pea': pe,
                            't3': 'Using load life relationship,',
                            'l10': 'L10 (mRev)',
                            'l10a': mlRevL10 ,
                            'cd': 'Dynamic C (N)',
                            'cda': dynamicC2 ,
                            'cal': 'Calculation:',
                        }
            
                else:
                    print("inside if chgcelk 44444444444")
                    dget=cursor.fetchall()
                    cdb="SELECT * FROM series64 where d >= (SELECT dia FROM dgbbip1 ORDER BY no DESC LIMIT 1);"
                    
                    cursor.execute(cdb)
                    cget=cursor.fetchone()
                    print("after cget")
                    print(cget)
                    staticC=cget[8]
                    dynamicC=cget[9]
                    print(staticC)
                    print(dynamicC)
                    dget=cursor.fetchall()
                    faByStaticC=round(int(fa) / staticC,3)
                    print(faByStaticC)
                    faByFr=round( int(fa) / int(fr),3)
                    print(faByFr)
                    faco = (faByStaticC,)
                    ddb="SELECT * FROM dgbb.eqbrgload WHERE faco >= '%f'" % faco
                    cursor.execute(ddb)
                    dget=cursor.fetchone()
                    
                    e=dget[1]
                    print(e)

                    if faByFr > e:
                        xyval=' Fa/Fr is greater than e'
                        #print("inside if")
                        gx=dget[4]
                        gy=dget[5]
                        #print(e,gx,gy)
                    else:
                        xyval=' Fa/Fr is less or equal to e'
                        gx=dget[2]
                        gy=dget[3]
                        
                    pe=round((gx* int(fr)+ gy* int(fa))* float(ka),2)
                    print(pe)
                    mlRevL10=(int(lyf)*60* int(n)) / 1000000
                    print(mlRevL10)
                        
                    dynamicC2=round(round(mlRevL10 ** (1. / 3),2) * pe,2)
                    print(dynamicC2)
                    print(staticC)
                    if dynamicC2 <= dynamicC:
                        ansvs={
                            'op': 'YOUR BEARING OF BASIC DESIGN NO: (SKF)',
                            'skfr': 'SKF',
                            'skf': cget[0],
                            'dr': 'd (mm)',
                            'd': cget[1],
                            'd1r': 'D1 Min. (mm)',
                            'D1': cget[2],
                            'drr': 'D (mm)',
                            'D': cget[3],
                            'd2r': 'D2 Min. (mm)',
                            'D2': cget[4],
                            'br': 'B (mm)',
                            'B': cget[5],
                            'rr': 'r (mm)',
                            'r': cget[6],
                            'r1r': 'r1 (mm)',
                            'r1': cget[7],
                            'cor': 'Static Co (N)',
                            'co': cget[8],
                            'cr':'Dynamic C (N)',
                            'c': cget[9],
                            'spr': 'Max. Speed (rpm)',
                            'sp': cget[10],
                            't1':'Selection od radial and thrust factors:',
                            'fbc': 'Fa/Co',
                            'fbca': faByStaticC ,
                            'fafr': 'Fa/Fr   taking V=1',
                            'fafra': faByFr ,
                            'echk': xyval,
                            'xx': 'X',
                            'xxa': gx,
                            'yy': 'Y',
                            'yya': gy,
                            't2': 'Equivalent Dynamic Load:',
                            'pes': 'Pe (N)',
                            'pea': pe,
                            't3': 'Using load life relationship,',
                            'l10': 'L10 (mRev)',
                            'l10a': mlRevL10 ,
                            'cd': 'Dynamic C (N)',
                            'cda': dynamicC2 ,
                            'cal': 'Calculation:',
                        }
            
                    else:
                        ansvs={
                            'skf': "all conditions failed."
                        }



    return render(request, 'dgbbip.html',ansvs)
