"""Exceções de domínio da aplicação."""


class ProcessCancelled(Exception):
    """Usuário solicitou cancelamento cooperativo; não indica bug."""
