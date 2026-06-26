
class RegraNegocioException(Exception):
    pass

def validar_obrigatorios(campos: dict):
    for nome_campo, valor in campos.items():
        if valor is None or (isinstance(valor, str) and not valor.strip()):
            raise RegraNegocioException(f"O campo '{nome_campo}' é obrigatório.")

def validar_tipo(objeto, tipo_esperado):
    if not isinstance(objeto, tipo_esperado):
        raise RegraNegocioException(f"O objeto/campo não corresponde ao tipo esperado.")
