class Mapper:
    def get_mapper(self):
        return {
            'loginUsuario': 'login',
            'nomeUsuario': 'name',
            'tipoUsuario': 'user_type',
            'emailPrincipalUsuario': 'main_email',
            'emailAlternativoUsuario': 'alternative_email',
            'emailUspUsuario': 'usp_email',
            'numeroTelefoneFormatado': 'formatted_phone',
            'wsuserid': 'wsuserid',
            'vinculo': 'bind'
        }


class Transform:
    mapper = None
