def parse_packet(packet):
  parts = packet.split(":")
  if len(parts) > 5:
      return {
          "version": parts[0],
          "packet_number": parts[1],
          "sender": parts[2],
          "host": parts[3],
          "command": parts[4],
          "message": parts[5]
      }
  return None

def create_packet(version, packet_number, sender, host, command, message):
  return f"{version}:{packet_number}:{sender}:{host}:{command}:{message}"
