import requests
import pandas as pd
from prettytable import PrettyTable

headers = {
    "Host": "zw.cdzj.chengdu.gov.cn",
    "Origin": "https://zw.cdzj.chengdu.gov.cn",
    "Content-Type": "application/x-www-form-urlencoded",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.75 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
    "Referer": "https://zw.cdzj.chengdu.gov.cn/lottery/accept/projectList",
    "Accept-Encoding": "gzip, deflate, br",
    "Cookie": "JSESSIONID=043A9EBF069AEB25FEF3A0D6CD5D848C; route=bdec837c7e1c29abc7e4a1324bbfe784",
}


def get_data():
    tables = []
    for i in range(10):
        r = requests.post(
            f"https://zw.cdzj.chengdu.gov.cn/lottery/accept/projectList?pageNo={i+1}&regioncode=00", headers=headers)
        if "<td>正在报名</td>" in r.text:
            table = pd.read_html(r.text, encoding='utf-8')
            tables.append(table[1])
        elif "<td>未报名</td>" in r.text:
            table = pd.read_html(r.text, encoding='utf-8')
            tables.append(table[1])
        else:
            break
    df = pd.concat(tables)
    df = df[df['项目报名状态'] != "报名结束"]
    return df


if __name__ == "__main__":
    while True:
        try:
            df = get_data()
            df = df.sort_values(by="区域")
            df = df.sort_values(by="登记结束时间")
            col_names = ['区域', '项目名称', '住房套数',
                         '登记开始时间', '登记结束时间', '选房结束时间', '项目报名状态']
            table = PrettyTable(col_names)
            for row in df[col_names].iterrows():
                table.add_row(list(row[1]))
            print(table)
            print(f"目前有 {len(df)} 个楼盘正在报名摇号")
            print(f"前往登记（9:00-18:00）：https://zw.cdzj.chengdu.gov.cn/lottery/accept/index")
            break
        except:
            pass
