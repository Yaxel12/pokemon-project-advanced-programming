game_status = 'select pokemon'
while game_status != 'quit':
    for event in pygame.event.get():
        if event.type == QUIT:
            game_status = 'quit'
        if event.type == KEYDOWN:
            if event.key == K_y:
                pokemons = [Pokemon('Bulbasaur', level), Pokemon('Charmander', level), Pokemon('Squirtle', level)]
                game_status = 'select pokemon'
            elif event.key == K_n:
                game_status = 'quit'
        if event.type == MOUSEBUTTONDOWN:
            mouse_click = event.pos
            if game_status == 'select pokemon':
                for i, pokemon in enumerate(pokemons):
                    if pokemon.get_rect().collidepoint(mouse_click):
                        player_pokemon = pokemons[i]
                        rival_pokemon = pokemons[(i + 1) % len(pokemons)]
                        rival_pokemon.level = int(rival_pokemon.level * .75)
                        player_pokemon.set_stats()
                        rival_pokemon.set_stats()
                        game_status = 'prebattle'
    if game_status == 'select pokemon':
        game.fill(white)
        for pokemon in pokemons:
            pokemon.draw()
        mouse_cursor = pygame.mouse.get_pos()
        for pokemon in pokemons:
            if pokemon.get_rect().collidepoint(mouse_cursor):
                pygame.draw.rect(game, black, pokemon.get_rect(), 2)
        pygame.display.update()
    # El resto de la lógica del juego se gestionaría en este controlador
