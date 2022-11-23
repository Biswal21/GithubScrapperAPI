import requests, math, time, os


def get_user_profile_urls(page_count, query_data, last_page, token_id):
    total_user_urls = []
    half_page_count = math.ceil(page_count / 2)
    for i in range(half_page_count):
        if i != 0 and i % 10 == 0:
            time.sleep(5)
        # Asc fetch
        query_data["page"] = i + 1
        query_data["order"] = "asc"
        try:
            response = requests.get(
                os.environ.get("GITHUB_USER_API"),
                params=query_data,
                headers=token_id,
            )
            if response.status_code in [404, 400, 422, 403, 503]:
                raise Exception
            else:
                asc_response = response.json()
        except Exception as e:
            return [], True, response.status_code
        asc_items = asc_response["items"]
        # Desc fetch
        query_data["order"] = "desc"
        try:
            response = requests.get(
                os.environ.get("GITHUB_USER_API"),
                params=query_data,
                headers=token_id,
            )
            if response.status_code in [404, 400, 422, 503, 403]:
                raise Exception
            else:
                desc_response = response.json()
        except Exception as e:
            return [], True, response.status_code
        desc_items = desc_response["items"]

        if i == (half_page_count - 1):
            if i == 0:
                total_user_urls.extend([item["url"] for item in asc_items])
                total_user_urls.extend([item["url"] for item in desc_items])
            elif (i - 1) % 2 == 0:
                total_user_urls.extend([item["url"] for item in asc_items])
                desc = [item["url"] for item in desc_items]
                total_user_urls.extend(desc[:last_page])
            elif (i - 1) % 2 != 0:
                desc = [item["url"] for item in desc_items]
                total_user_urls.extend(desc[:last_page])
        else:
            total_user_urls.extend([item["url"] for item in asc_items])
            total_user_urls.extend([item["url"] for item in desc_items])

    return total_user_urls, False, ""


def get_users_profile_data(user_urls, token_id):
    profile_data_list = []
    for req_turn, url in enumerate(user_urls):
        if req_turn != 0 and req_turn % 10 == 0:
            time.sleep(5)  # To avoid getting forbid by Github API

        try:
            response = requests.get(url=url, headers=token_id)
        except:
            return [], True, response.status_code

        data = response.json()
        user_profle = {}
        user_profle["name"] = data["name"]
        user_profle["github_handle"] = data["login"]
        user_profle["blurb"] = data["bio"]
        user_profle["location"] = data["location"]
        user_profle["github_profile_link"] = data["html_url"]

        if data["twitter_username"] is not None:
            user_profle["twitter_handle"] = data["twitter_username"]
        else:
            user_profle["twitter_handle"] = ""
        if data["email"] is not None:
            user_profle["email"] = data["email"]
        else:
            user_profle["email"] = ""
        profile_data_list.append(user_profle)

    return profile_data_list, False, ""
