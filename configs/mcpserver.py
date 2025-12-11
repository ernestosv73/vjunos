from fastmcp import FastMCP
import subprocess

# -----------------------------------------------------------------------------
#   Servidor FastMCP dedicado a herramientas THC-IPv6
# -----------------------------------------------------------------------------
mcp = FastMCP("THC IPv6 Security Toolkit Server")


# -----------------------------------------------------------------------------
#   Helper interno para ejecutar comandos del sistema
# -----------------------------------------------------------------------------
def run_cmd(cmd: list[str]) -> str:
    """
    Ejecuta un comando y devuelve stdout o el error capturado.
    """
    try:
        output = subprocess.check_output(
            cmd, stderr=subprocess.STDOUT, text=True
        )
        return output
    except subprocess.CalledProcessError as e:
        return f"[ERROR]\nCommand: {' '.join(cmd)}\nOutput:\n{e.output}"


# -----------------------------------------------------------------------------
#   1. Wrapper genérico: ejecutar cualquier herramienta THC-IPv6
# -----------------------------------------------------------------------------
@mcp.tool
def thc6(command: str, args: list[str]) -> str:
    """
    Ejecuta cualquier herramienta THC-IPv6.
    Ejemplo:
      thc6("alive6", ["eth0", "fe80::1"])
    """
    cmd = [command] + args
    return run_cmd(cmd)


# -----------------------------------------------------------------------------
#   2. alive6 – Descubrimiento de hosts IPv6
# -----------------------------------------------------------------------------
@mcp.tool
def alive6(iface: str, target: str) -> str:
    """Descubre hosts IPv6 activos usando alive6."""
    return run_cmd(["alive6", iface, target])


# -----------------------------------------------------------------------------
#   3. thcping6 – Ping avanzado
# -----------------------------------------------------------------------------
@mcp.tool
def thcping6(src: str, iface: str, dst: str) -> str:
    """Ejecuta thcping6 enviando paquetes ICMPv6 custom."""
    return run_cmd(["thcping6", "-F", src, iface, "x", dst])


# -----------------------------------------------------------------------------
#   4. detect-new-ip6 – Detecta nuevos hosts IPv6 en la red
# -----------------------------------------------------------------------------
@mcp.tool
def detect_new_ip6(iface: str) -> str:
    """Detecta nuevos nodos IPv6 apareciendo en la red."""
    return run_cmd(["detect-new-ip6", iface])


# -----------------------------------------------------------------------------
#   5. flood_router6 – Ataque de flooding a routers IPv6
# -----------------------------------------------------------------------------
@mcp.tool
def flood_router6(iface: str) -> str:
    """Inunda un router IPv6 con RA (usado para pruebas de seguridad)."""
    return run_cmd(["flood_router6", iface])


# -----------------------------------------------------------------------------
#   6. dos-new-ip6 – DoS contra sistema de asignación de IPv6
# -----------------------------------------------------------------------------
@mcp.tool
def dos_new_ip6(iface: str, target: str) -> str:
    """DoS contra detección de nuevas direcciones IPv6."""
    return run_cmd(["dos-new-ip6", iface, target])


# -----------------------------------------------------------------------------
#   7. fake_router6 – Enviar Router Advertisements falsos
# -----------------------------------------------------------------------------
@mcp.tool
def fake_router6(iface: str, prefix: str) -> str:
    """Envía RA falsos con un prefijo arbitrario."""
    return run_cmd(["fake_router6", iface, prefix])


# -----------------------------------------------------------------------------
#   8. parasite6 – Envenenamiento de cache ND
# -----------------------------------------------------------------------------
@mcp.tool
def parasite6(iface: str, victim: str, router: str) -> str:
    """Ataque ND Spoofing con parasite6."""
    return run_cmd(["parasite6", iface, victim, router])


# -----------------------------------------------------------------------------
#   9. exploit6 – Módulo multipropósito de explotación
# -----------------------------------------------------------------------------
@mcp.tool
def exploit6(iface: str, dst: str) -> str:
    """Ejecuta exploit6 hacia un destino."""
    return run_cmd(["exploit6", iface, dst])


# -----------------------------------------------------------------------------
#   10. flood_advertise6 – Envía múltiples NA
# -----------------------------------------------------------------------------
@mcp.tool
def flood_advertise6(iface: str, target: str) -> str:
    """Envía un flood de Neighbor Advertisements."""
    return run_cmd(["flood_advertise6", iface, target])


# -----------------------------------------------------------------------------
#   11. dump_router6 – Analiza mensajes router en la red
# -----------------------------------------------------------------------------
@mcp.tool
def dump_router6(iface: str) -> str:
    """Escucha y analiza RA/RS en la red."""
    return run_cmd(["dump_router6", iface])


# -----------------------------------------------------------------------------
#   ARRANQUE DEL SERVIDOR (IMPORTANTE PARA DOCKER)
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    try:
        mcp.run(transport="streamable-http", host="0.0.0.0", port=3000, path="/mcp")
    except Exception as e:
        print(f"Error: {e}")

