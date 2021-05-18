import json
import logging

import requests


class YggdrasilSessionServer:
    """
    Yggdrasil session server interface
    """

    # def authenticate(self, form) -> (str, int):
    #     """
    #     登录
    #     POST /authserver/authenticate
    #     使用密码进行身份验证，并分配一个新的令牌。
    #     请求格式：
    #     {
    #         "username":"邮箱（或其他凭证，详见 §使用角色名称登录）",
    #         "password":"密码",
    #         "clientToken":"由客户端指定的令牌的 clientToken（可选）",
    #         "requestUser":true/false, // 是否在响应中包含用户信息，默认 false
    #         "agent":{
    #             "name":"Minecraft",
    #             "version":1
    #         }
    #     }
    #     若请求中未包含 clientToken，服务端应该随机生成一个无符号 UUID 作为 clientToken。
    #     但需要注意 clientToken 可以为任何字符串，即请求中提供任何 clientToken 都是可以接
    #     受的，不一定要为无符号 UUID。
    #     对于令牌要绑定的角色：若用户没有任何角色，则为空；若用户仅有一个角色，那么通常绑定到该
    #     角色；若用户有多个角色，通常为空，以便客户端进行选择。也就是说如果绑定的角色为空，则需
    #     要客户端进行角色选择。
    #     响应格式：
    #     {
    #         "accessToken":"令牌的 accessToken",
    #         "clientToken":"令牌的 clientToken",
    #         "availableProfiles":[ // 用户可用角色列表
    #             // ,... 每一项为一个角色（格式见 §角色信息的序列化）
    #         ],
    #         "selectedProfile":{
    #             // ... 绑定的角色，若为空，则不需要包含（格式见 §角色信息的序列化）
    #         },
    #         "user":{
    #             // ... 用户信息（仅当请求中 requestUser 为 true 时包含，格式见 §用户信息的序列化）
    #         }
    #     }
    #     安全提示： 该 API 可以被用于密码暴力破解，应受到速率限制。限制应针对用户，而不是客户端 IP。
    #     使用角色名称登录
    #     除使用邮箱登录外，验证服务器还可以允许用户使用角色名称登录。要实现这一点，验证服务器需要进行以下工作：
    #
    #     将 API 元数据中的 feature.non_email_login 字段设置为 true。（见 API 元数据获取§功能选项）
    #     接受在登录接口中使用角色名称作为 username 参数。
    #     当用户使用角色名称登录时，验证服务器应自动将令牌绑定到相应角色，即上文响应中的 selectedProfile
    #     应为用户登录时所用的角色。
    #     这种情况下，如果用户拥有多个角色，那么他可以省去选择角色的操作。考虑到某些程序不支持多角色
    #     （例如 Geyser），还可以通过上述方法绕过角色选择。
    #
    #     :param form:
    #     :return:
    #     """
    #     raise NotImplementedError()
    #
    # def refresh(self, form) -> (str, int):
    #     """
    #     刷新
    #     POST /authserver/refresh
    #     吊销原令牌，并颁发一个新的令牌。
    #     请求格式：
    #     {
    #         "accessToken":"令牌的 accessToken",
    #         "clientToken":"令牌的 clientToken（可选）",
    #         "requestUser":true/false, // 是否在响应中包含用户信息，默认 false
    #         "selectedProfile":{
    #             // ... 要选择的角色（可选，格式见 §角色信息的序列化）
    #         }
    #     }
    #     当指定 clientToken 时，服务端应检查 accessToken 和 clientToken 是否有效，
    #     否则只需要检查 accessToken。
    #     颁发的新令牌的 clientToken 应与原令牌的相同。
    #     如果请求中包含 selectedProfile，那么这就是一个选择角色的操作。此操作要求原令
    #     牌所绑定的角色为空，而新令牌则将绑定到 selectedProfile 所指定的角色上。如果
    #     不包含 selectedProfile，那么新令牌所绑定的角色和原令牌相同。
    #     刷新操作在令牌暂时失效时依然可以执行。若请求失败，原令牌依然有效。
    #     响应格式：
    #     {
    #         "accessToken":"新令牌的 accessToken",
    #         "clientToken":"新令牌的 clientToken",
    #         "selectedProfile":{
    #             // ... 新令牌绑定的角色，若为空，则不需要包含（格式见 §角色信息的序列化）
    #         },
    #         "user":{
    #             // ... 用户信息（仅当请求中 requestUser 为 true 时包含，格式见 §用户信息的序列化）
    #         }
    #     }
    #     :param form:
    #     :return:
    #     """
    #     raise NotImplementedError()
    #
    # def validate(self, form) -> (str, int):
    #     """
    #     验证令牌
    #     POST /authserver/validate
    #     检验令牌是否有效。
    #     请求格式：
    #     {
    #         "accessToken":"令牌的 accessToken",
    #         "clientToken":"令牌的 clientToken（可选）"
    #     }
    #     当指定 clientToken 时，服务端应检查 accessToken 和 clientToken 是否有效，
    #     否则只需要检查 accessToken 。
    #     若令牌有效，服务端应返回 HTTP 状态 204 No Content，否则作为令牌无效的异常情况处理。
    #     :param form:
    #     :return:
    #     """
    #     raise NotImplementedError()
    #
    # def invalidate(self, form) -> (str, int):
    #     """
    #     POST /authserver/invalidate
    #     吊销给定令牌。
    #     请求格式：
    #     {
    #         "accessToken":"令牌的 accessToken",
    #         "clientToken":"令牌的 clientToken（可选）"
    #     }
    #     服务端只需要检查 accessToken，即无论 clientToken 为何值都不会造成影响。
    #     无论操作是否成功，服务端应返回 HTTP 状态 204 No Content。
    #     :param form:
    #     :return:
    #     """
    #     raise NotImplementedError()
    #
    # def signout(self, form) -> (str, int):
    #     """
    #     POST /authserver/signout
    #     吊销用户的所有令牌。
    #     请求格式：
    #     {
    #         "username":"邮箱",
    #         "password":"密码"
    #     }
    #     若操作成功，服务端应返回 HTTP 状态 204 No Content。
    #     安全提示： 该 API 也可用于判断密码的正确性，因此应受到和登录 API 一样的速率限制。
    #     :param form:
    #     :return:
    #     """
    #     raise NotImplementedError()

    def join(self, form) -> (str, int):
        """
        客户端进入服务器
        POST /session/minecraft/join
        记录服务端发送给客户端的 serverId，以备服务端检查。
        请求格式：
        {
            "accessToken":"令牌的 accessToken",
            "selectedProfile":"该令牌绑定的角色的 UUID（无符号）",
            "serverId":"服务端发送给客户端的 serverId"
        }
        仅当 accessToken 有效，且 selectedProfile 与令牌所绑定的角色一致时，操作才成功。
        服务端应记录以下信息：
        serverId
        accessToken
        发送该请求的客户端 IP
        实现时请注意：以上信息应记录在内存数据库中（如 Redis），且应该设置过期时间（如 30 秒）。
        介于 serverId 的随机性，可以将其作为主键。
        若操作成功，服务端应返回 HTTP 状态 204 No Content。
        :param form:
        :return:
        """
        raise NotImplementedError()

    def hasJoined(self, form) -> (str, int):
        """
        服务端验证客户端
        GET /session/minecraft/hasJoined?username={username}&serverId={serverId}&ip={ip}
        检查客户端会话的有效性，即数据库中是否存在该 serverId 的记录，且信息正确。
        请求参数：
        参数	值
        username	角色的名称
        serverId	服务端发送给客户端的 serverId
        ip （可选）	Minecraft 服务端获取到的客户端 IP，仅当 prevent-proxy-connections 选项开启时包含
        username 需要与 serverId 所对应令牌所绑定的角色的名称相同。
        响应格式：
        {
            // ... 令牌所绑定角色的完整信息（包含角色属性及数字签名，格式见 §角色信息的序列化）
        }
        若操作失败，服务端应返回 HTTP 状态 204 No Content。
        :param form:
        :return:
        """
        raise NotImplementedError()

    def profile(self, form) -> (str, int):
        """
        GET /session/minecraft/profile/{uuid}?unsigned={unsigned}
        查询指定角色的完整信息（包含角色属性）。
        请求参数：
        参数	值
        uuid	角色的 UUID（无符号）
        unsigned （可选）	true 或 false。是否在响应中不包含数字签名，默认为 true
        响应格式：
        {
            // ... 角色信息（包含角色属性。若 unsigned 为 false，还需要包含数字签名。格式见 §角色信息的序列化）
        }
        若角色不存在，服务端应返回 HTTP 状态 204 No Content。
        :param form:
        :return:
        """
        raise NotImplementedError()


class ConcreteYggdrasilSessionServer(YggdrasilSessionServer):

    def __init__(self, server_url: str):
        if not server_url.endswith('/'):
            server_url += '/'
        self._server_url = server_url

    def __str__(self):
        return self.get_server_url()

    def join(self, form) -> (str, int):
        return self._form_request(self._url_join(), form)

    def hasJoined(self, form) -> (str, int):
        return self._form_request(self._url_has_joined(), form)

    def profile(self, form) -> (str, int):
        return self._form_request(self._url_profile(), form)

    def get_server_url(self) -> str:
        return self._server_url

    def _url_has_joined(self):
        return self._server_url + 'sessionserver/session/minecraft/hasJoined'

    def _url_join(self):
        return self._server_url + 'sessionserver/session/minecraft/join'

    def _url_profile(self):
        return self._server_url + 'sessionserver/session/minecraft/profile'

    def _form_request(self, url, form, method='GET') -> (str, int):
        try:
            method = method.upper()
            logging.debug(f'Make request with form {json.dumps(form)}')
            if method == 'GET':
                r = requests.get(url, params=form, timeout=3, headers={'User-Agent': 'Java/1.8.0_271'})
            elif method == 'POST':
                r = requests.post(url, data=json.dumps(form), headers={
                    'Content-Type': 'application/json',
                    'User-Agent': 'Java/1.8.0_271'
                }, timeout=3)
            else:
                raise ValueError(f'Unsupported method {method}')
            logging.debug(
                f'Form request returns (status_code={r.status_code}, headers={"".join([f"{k}: {v}; " for k, v in r.headers.items()])}'
                f', text={r.text})')
            return r.text, r.status_code
        except IOError as e:
            logging.error(f'Failed to {method} url {url} with form {form}: {e}')
            return '', 500


class MojangYggdrasilSessionServer(ConcreteYggdrasilSessionServer):

    def _url_has_joined(self):
        return self._server_url + 'session/minecraft/hasJoined'

    def _url_join(self):
        return self._server_url + 'session/minecraft/join'

    def _url_profile(self):
        return self._server_url + 'session/minecraft/profile'


def is_mojang_yggdrasil_server(url: str):
    return url in ('https://sessionserver.mojang.com',
                   'http://sessionserver.mojang.com',
                   'sessionserver.mojang.com')


class YggdrasilServerBuilder:

    @staticmethod
    def from_root_url(url: str):
        """
        Create a Yggdrasil server from its root API url.
        Accept both official and 3rd-party (defined in authlib-injector wiki) server.
        :param url: the API root.
        :return: the server instance.
        """

        if is_mojang_yggdrasil_server(url):
            return MojangYggdrasilSessionServer(server_url=url)
        else:
            return ConcreteYggdrasilSessionServer(server_url=url)
