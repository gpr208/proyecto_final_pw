def test_pagina_principal(client):
    respuesta = client.get("/")

    assert respuesta.status_code == 200
    assert b"MOE'S BAR" in respuesta.data
    assert "Categorías".encode("utf-8") in respuesta.data
    assert "Meseros".encode("utf-8") in respuesta.data