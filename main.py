from models.system_state import EclipseState


def main():
    eclipse = EclipseState()

    print("ECLIPSE starting...")
    print(eclipse)

    eclipse.battery_percent = 83
    eclipse.lens_tint_percent = 24

    eclipse.phone.connected = True

    eclipse.phone.media.playing = True
    eclipse.phone.media.title = "Blinding Lights"
    eclipse.phone.media.artist = "The Weekend"

    eclipse.phone.message.active = True
    eclipse.phone.message.sender = "Alex"
    eclipse.phone.message.text = "Are you almost here?"



    print()
    print("Updated ECLIPSE state:")
    print(eclipse)


if __name__ == "__main__":
    main()