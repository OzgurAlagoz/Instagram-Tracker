from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import json
from account import instauser,instapass
import os
import shutil
from jsondiff import diff

driver=webdriver.Firefox()

driver.get("https://www.instagram.com/")
driver.maximize_window()

currentWd = os.getcwd()
files = os.listdir(currentWd)
mainFile = '{}.json'.format(instauser)
checkFile = '{}_check.json'.format(instauser)

new_followers = []
new_followings = []

def write_json(new_data, dataname, filename=mainFile):
    with open(filename,'r+',encoding = 'utf-8') as file:
        file_data = json.load(file)
        if new_data not in file_data[dataname]:
            file_data[dataname].append(new_data)
            file.seek(0)
            file.truncate()
            json.dump(file_data, file, indent = 4,ensure_ascii=False)

def jsonSkeletonWrite():
    try:
        with open(mainFile, "r+", encoding="utf-8") as newfile:
            try:
                file_data = json.load(newfile)
            except json.JSONDecodeError:
                file_data = {}

            if "followers" not in file_data:
                file_data["followers"] = []
            if "following" not in file_data:
                file_data["following"] = []

            newfile.seek(0)
            json.dump(file_data, newfile, indent=4, ensure_ascii=False)
            newfile.truncate()

    except FileNotFoundError:
        with open(mainFile, "w", encoding="utf-8") as newfile:
            json.dump({"followers": [], "following": []}, newfile, indent=4, ensure_ascii=False)


def readJSON(filename=mainFile):
    with open(filename, 'r+', encoding='utf-8') as file:
        file_data = json.load(file)
    return file_data

def update_json(new_data, new_data2, dataname, dataname2, filename=mainFile):
    file_data = readJSON(filename)

    existing_data = {entry["username"] for entry in file_data[dataname]}
    existing_data2 = {entry2["username"] for entry2 in file_data[dataname2]}
    
    new_data_usernames = {entry["username"] for entry in new_data}
    new_data_usernames2 = {entry2["username"] for entry2 in new_data2}

    new_entries = [entry for entry in new_data if entry["username"] not in existing_data]
    new_entries2 = [entry2 for entry2 in new_data2 if entry2["username"] not in existing_data2]

    removed_entries = {entry["username"] for entry in file_data[dataname] if entry["username"] not in new_data_usernames}
    removed_entries2 = {entry2["username"] for entry2 in file_data[dataname2] if entry2["username"] not in new_data_usernames2}

    file_data[dataname] = [entry for entry in file_data[dataname] if entry["username"] not in removed_entries]
    file_data[dataname].extend(new_entries)

    file_data[dataname2] = [entry2 for entry2 in file_data[dataname2] if entry2["username"] not in removed_entries2]
    file_data[dataname2].extend(new_entries2)

    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(file_data, file, indent=4, ensure_ascii=False)
    
    return new_entries, new_entries2, removed_entries, removed_entries2


def getDataFromPage():
    username = driver.find_element(By.XPATH, "/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div/section/main/article/div[2]/div[1]/div[2]/div/form/div[1]/div[1]/div/label/input")
    username.send_keys(instauser)
    password = driver.find_element(By.XPATH,"/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div/section/main/article/div[2]/div[1]/div[2]/div/form/div[1]/div[2]/div/label/input")
    password.send_keys(instapass)
    login = driver.find_element(By.XPATH,"/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div/section/main/article/div[2]/div[1]/div[2]/div/form/div[1]/div[3]").click()
    time.sleep(8)
    driver.get("https://www.instagram.com/{}".format(instauser))
    time.sleep(5)
    followers = driver.find_element(By.XPATH,"/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[2]/div/div[1]/section/main/div/header/section[3]/ul/li[2]/div/a").click()
    time.sleep(5)
    followersList = driver.find_element(By.XPATH,"/html/body/div[5]/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]/div[1]").find_elements(By.CSS_SELECTOR,".x9f619.xjbqb8w.x78zum5.x168nmei.x13lgxp2.x5pf9jr.xo71vjh.x1n2onr6.x1plvlek.xryxfnj.x1c4vz4f.x2lah0s.x1q0g3np.xqjyukv.x6s0dn4.x1oa3qoh.x1nhvcw1")
    followersName = driver.find_element(By.XPATH,"/html/body/div[5]/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]/div[1]").find_elements(By.CSS_SELECTOR,".x1lliihq.x1plvlek.xryxfnj.x1n2onr6.x1ji0vk5.x18bv5gf.x193iq5w.xeuugli.x1fj9vlw.x13faqbe.x1vvkbs.x1s928wv.xhkezso.x1gmr53x.x1cpjm7i.x1fgarty.x1943h6x.x1i0vuye.xvs91rp.xo1l8bm.x1roi4f4.x10wh9bi.x1wdrske.x8viiok.x18hxmgj")

    for a, b in zip(followersName, followersList):
        user = {"name" : a.text, "username" : b.text}
        new_followers.append(user)
        write_json(user,"followers")

    scrollBar = driver.find_element(By.XPATH,"/html/body/div[5]/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]")
    last_height = driver.execute_script("return arguments[0].scrollHeight", scrollBar)
    SCROLL_PAUSE_TIME = 3
    while True:
        driver.execute_script("arguments[0].scrollBy(0, arguments[0].scrollHeight);", scrollBar)
        time.sleep(SCROLL_PAUSE_TIME)
        followersList2 = driver.find_element(By.XPATH,"/html/body/div[5]/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]/div[1]").find_elements(By.CSS_SELECTOR,".x9f619.xjbqb8w.x78zum5.x168nmei.x13lgxp2.x5pf9jr.xo71vjh.x1n2onr6.x1plvlek.xryxfnj.x1c4vz4f.x2lah0s.x1q0g3np.xqjyukv.x6s0dn4.x1oa3qoh.x1nhvcw1")
        followersName2 = driver.find_element(By.XPATH,"/html/body/div[5]/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]/div[1]").find_elements(By.CSS_SELECTOR,".x1lliihq.x1plvlek.xryxfnj.x1n2onr6.x1ji0vk5.x18bv5gf.x193iq5w.xeuugli.x1fj9vlw.x13faqbe.x1vvkbs.x1s928wv.xhkezso.x1gmr53x.x1cpjm7i.x1fgarty.x1943h6x.x1i0vuye.xvs91rp.xo1l8bm.x1roi4f4.x10wh9bi.x1wdrske.x8viiok.x18hxmgj")
        for (j,k) in zip(followersName2,followersList2): 
            user2 = {"name": j.text,"username": k.text} 
            if user2 not in new_followers:
                new_followers.append(user2)
                write_json(user2,"followers")

        new_height = driver.execute_script("return arguments[0].scrollHeight", scrollBar)
        if new_height == last_height:
            break
        else:
            last_height = new_height
    
    driver.get("https://www.instagram.com/{}".format(instauser))
    time.sleep(2)
    following = driver.find_element(By.XPATH, "/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[2]/div/div[1]/section/main/div/header/section[3]/ul/li[3]/div/a").click()
    time.sleep(2)
    followingList = driver.find_element(By.XPATH,"/html/body/div[5]/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]/div[1]").find_elements(By.CSS_SELECTOR,".x9f619.xjbqb8w.x78zum5.x168nmei.x13lgxp2.x5pf9jr.xo71vjh.x1n2onr6.x1plvlek.xryxfnj.x1c4vz4f.x2lah0s.x1q0g3np.xqjyukv.x6s0dn4.x1oa3qoh.x1nhvcw1")
    followingName = driver.find_element(By.XPATH,"/html/body/div[5]/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]/div[1]").find_elements(By.CSS_SELECTOR,".x1lliihq.x1plvlek.xryxfnj.x1n2onr6.x1ji0vk5.x18bv5gf.x193iq5w.xeuugli.x1fj9vlw.x13faqbe.x1vvkbs.x1s928wv.xhkezso.x1gmr53x.x1cpjm7i.x1fgarty.x1943h6x.x1i0vuye.xvs91rp.xo1l8bm.x1roi4f4.x10wh9bi.x1wdrske.x8viiok.x18hxmgj")
    for x, y in zip(followingName, followingList):
        user3 = {"name": x.text,"username" : y.text}
        new_followings.append(user3)
        write_json(user3,"following")

    scrollBar2 = driver.find_element(By.XPATH,"/html/body/div[5]/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]")
    last_height2 = driver.execute_script("return arguments[0].scrollHeight", scrollBar2)
    SCROLL_PAUSE_TIME = 3
    while True:
        driver.execute_script("arguments[0].scrollBy(0, arguments[0].scrollHeight);", scrollBar2)
        time.sleep(SCROLL_PAUSE_TIME)
        followingList2 = driver.find_element(By.XPATH,"/html/body/div[5]/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]/div[1]").find_elements(By.CSS_SELECTOR,".x9f619.xjbqb8w.x78zum5.x168nmei.x13lgxp2.x5pf9jr.xo71vjh.x1n2onr6.x1plvlek.xryxfnj.x1c4vz4f.x2lah0s.x1q0g3np.xqjyukv.x6s0dn4.x1oa3qoh.x1nhvcw1")
        followingName2 = driver.find_element(By.XPATH,"/html/body/div[5]/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]/div[1]").find_elements(By.CSS_SELECTOR,".x1lliihq.x1plvlek.xryxfnj.x1n2onr6.x1ji0vk5.x18bv5gf.x193iq5w.xeuugli.x1fj9vlw.x13faqbe.x1vvkbs.x1s928wv.xhkezso.x1gmr53x.x1cpjm7i.x1fgarty.x1943h6x.x1i0vuye.xvs91rp.xo1l8bm.x1roi4f4.x10wh9bi.x1wdrske.x8viiok.x18hxmgj")
        for (j,k) in zip(followingName2,followingList2): 
            user4 = {"name": j.text,"username": k.text}
            if user4 not in new_followings:
                new_followings.append(user4)
                write_json(user4,"following")

        new_height2 = driver.execute_script("return arguments[0].scrollHeight", scrollBar2)
        if new_height2 == last_height2:
            break
        else:
            last_height2 = new_height2
    return new_followers, new_followings
    
time.sleep(3)

if mainFile not in files:
    with open('{}.json'.format(instauser),"x+"):
        jsonSkeletonWrite()
        getDataFromPage()
        if checkFile not in files:
            time.sleep(5)
            shutil.copy('{}.json'.format(instauser),'{}_check.json'.format(instauser))
        else:
            pass
elif mainFile in files:
    new_followers, new_followings = getDataFromPage()
    time.sleep(3)
    update_json(new_followers, new_followings, "followers", "following")
    with open(mainFile, 'r+', encoding='utf-8') as f1, open(checkFile, 'r+', encoding='utf-8') as f2:
        json1 = json.load(f1)
        json2 = json.load(f2)
        print(diff(json1["followers"],json2["followers"]))
        print(diff(json1["following"],json2["following"]))
    if checkFile not in files:
            time.sleep(5)
            shutil.copy('{}.json'.format(instauser),'{}_check.json'.format(instauser))
    else:
        pass
else:
    print("Error")
        