# -*- coding: utf-8 -*-
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from pathlib import Path
import shutil

doc = docx.Document()

# Margenes
for s in doc.sections:
    s.top_margin = Inches(1)
    s.bottom_margin = Inches(1)
    s.left_margin = Inches(1)
    s.right_margin = Inches(1)

# Titulo Principal
p_title = doc.add_paragraph()
p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
run_title = p_title.add_run("Oni no Ketsuryū (鬼の血流 - La Estirpe de la Sangre)\nVolumen 6: Las Catacumbas del Olvido")
run_title.font.name = "Arial"
run_title.font.size = Pt(24)
run_title.font.bold = True
run_title.font.color.rgb = RGBColor(180, 0, 0)

# Subtitulo
p_sub = doc.add_paragraph()
p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
run_sub = p_sub.add_run("Obra Oficial por Nicolás Noguera\nEdición Digital Ilustrada")
run_sub.font.name = "Arial"
run_sub.font.size = Pt(14)
run_sub.font.italic = True

doc.add_page_break()

base_dir = Path(r"C:\Proyectos\mis-libros-editorial\libros\oni-no-ketsuryu-volumen-6")
dest2 = Path(r"c:\Users\nicol\Downloads\MIS LIBROS\libros\oni-no-ketsuryu-volumen-6")

base_dir.mkdir(parents=True, exist_ok=True)
dest2.mkdir(parents=True, exist_ok=True)

# Asignar imagenes base si falta alguna
ref_dir = Path(r"C:\Proyectos\mis-libros-editorial\libros\oni-no-ketsuryu-volumen-5")

all_imgs = [
    "portada.jpg", "thumbnail.jpg", "banner.jpg", "escena_1.jpg", "escena_climax.jpg",
    "escena_c1_e1.jpg", "escena_c1_e2.jpg", "escena_c1_e3.jpg",
    "escena_c2_e1.jpg", "escena_c2_e2.jpg", "escena_c2_e3.jpg",
    "escena_c3_e1.jpg", "escena_c3_e2.jpg", "escena_c3_e3.jpg",
    "escena_c4_e1.jpg", "escena_c4_e2.jpg", "escena_c4_e3.jpg",
    "escena_c5_e1.jpg", "escena_c5_e2.jpg", "escena_c5_e3.jpg"
]

for img_name in all_imgs:
    target1 = base_dir / img_name
    target2 = dest2 / img_name
    if not target1.exists():
        src = ref_dir / img_name
        if src.exists():
            shutil.copy(src, target1)
            shutil.copy(src, target2)

# Portada
portada_path = base_dir / "portada.jpg"
if portada_path.exists():
    doc.add_picture(str(portada_path), width=Inches(5.5))
    doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER
    doc.add_page_break()

# Texto del libro completo
capitulos = [
    {
        "titulo": "Capítulo 1: El Refugio de las Flores de Glicina",
        "escenas": [
            {
                "sub": "Escena 1: La Sede Oculta",
                "text": "Tras el milagro de la Aldea de los Herreros, el Gremio Cuervo trasladó a Miyuki y a Ren al santuario principal de la organización: una fortaleza antigua construida en el corazón de una caldera volcánica apagada, rodeada por un bosque impenetrable de floración de glicinas que brillaban bajo la luz de las estrellas.\n\nLos ocho Pilares supervivientes se reunieron en el salón principal frente al Líder Supremo del Gremio, un hombre de salud frágil pero de mirada profundamente sabia que vestía un kimono ceremonial blanco.\n\n—Miyuki ha logrado lo que ningún ser en mil años ha conseguido —habló el Líder Supremo con voz serena—. Pero esto significa que la cacería de Muzan ya no será en las sombras. Él vendrá con todo su ejército para devorarla.\n\nRen permanecía de pie al lado de su hermana, apretando la empuñadura de la Katana del Sol.\n\n—Que venga —respondió Ren—. Esta vez no nos esconderemos más.",
                "img": "escena_c1_e1.jpg"
            },
            {
                "sub": "Escena 2: El Secreto de la Marca",
                "text": "El Pilar del Acero y la Roca —Gyomei, un hombre gigante con un rosario budista entre sus manos y una cicatriz sobre los ojos ciegos— dio un paso al frente. Su aura emitía una presión física tan inmensa que la madera del suelo crujió ligeramente.\n\n—Para sobrevivir a la guerra que se avecina, todos los cazadores de rango superior deben manifestar la Marca del Sol —explicó Gyomei—. No es una simple cicatriz: se activa cuando la temperatura corporal supera los 39 grados y el ritmo cardíaco alcanza los 200 latidos por minuto durante un combate al límite.\n\nKanae y Muichiro miraron sus propias marcas en el cuello y la frente, recordando la sensación de haber estado al borde de la muerte durante sus respectivas batallas.\n\n—El problema —añadió Gyomei en voz baja— es que aquellos que despiertan la marca están pagando con su propia esperanza de vida... Ningún portador ha logrado superar los veinticinco años de edad.",
                "img": "escena_c1_e2.jpg"
            },
            {
                "sub": "Escena 3: El Entrenamiento de los Pilares",
                "text": "Sin dudarlo un segundo por el destino de su propia vida, Ren y los demás aceptaron someterse al Entrenamiento de la Marca: un régimen de preparación física e intensidad espartana dividido en cinco etapas, donde cada Pilar instruiría a la totalidad de las tropas del gremio.\n\nPrimera Etapa: Resistencia extrema bajo cascadas heladas con Gyomei.\nSegunda Etapa: Esgrima de alta velocidad y flexibilidad acrobática con Mitsuri.\nTercera Etapa: Movilidad táctica entre la niebla con Muichiro.\nCuarta Etapa: Corte de precisión y reflejos del trueno con Kaito.\nQuinta Etapa: Control de la presión arterial y respiración continua con el Pilar de la Piedra.\n\nRen comenzó la primera etapa cargando tres troncos de cedro sobre sus hombros bajo una cascada helada en mitad del invierno.",
                "img": "escena_c1_e3.jpg"
            }
        ]
    },
    {
        "titulo": "Capítulo 2: El Laberinto Bajo la Tierra",
        "escenas": [
            {
                "sub": "Escena 1: Las Catacumbas de la Tierra Antigua",
                "text": "Mientras el entrenamiento avanzaba, un equipo de exploración del gremio descubrió las ruinas del Santuario de los Tres Soles, un complejo de catacumbas subterráneas construido bajo la capital imperial donde se decía que reposaban los restos del primer herrero de la era Sengoku.\n\nRen, acompañado por Kaito (el cazador de la máscara de Tengu) y el chico del haori amarillo de la respiración del trueno, descendió por las escaleras de piedra de las catacumbas para buscar la Piedra de Afilado Solar, la única herramienta capaz de pulir la katana de Ren a su nivel definitivo.\n\nEl aire en el subterráneo olía a metal quemado y azufre antiguo.\n\n—Este lugar no ha sido tocado en cuatrocientos años —murmuró Kaito, manteniendo la mano en el pomo de su katana carmesí.",
                "img": "escena_c2_e1.jpg"
            },
            {
                "sub": "Escena 2: La Sombra del Primer Lunar",
                "text": "Al llegar a la cámara central de la catacumba, las antorchas de piedra se encendieron solas con una llama azulada.\n\nSentado en posición de meditación sobre un altar de piedra, los esperaba el guerrero más antiguo del imperio: Kokushibo, el Primer Lunar Rojo.\n\nSu sola presencia no producía miedo; producía una parálisis física absoluta. Vestía un kimono ceremonial de color púrpura oscuro, llevaba seis ojos con la marca del Primer Lunar en su rostro pálido y sosteniendo una katana cuya hoja de carne estaba cubierta por pequeñas pupilas que se movían buscando a sus presas.\n\n—Bien venido... descendiente del fuego... —habló Kokushibo con una voz profunda que hizo temblar las columnas de piedra—. Hacía siglos que no sentía la pulsación de la Respiración del Sol en la sangre de un humano.",
                "img": "escena_c2_e2.jpg"
            },
            {
                "sub": "Escena 3: El Pasado del Primer Lunar",
                "text": "Ren intentó desenvainar su katana, pero la presión del aura de Kokushibo le impidió mover un solo músculo.\n\n—Tú... eras el hermano gemelo del primer usuario del sol... —comprendió Ren, recordando los grabados de los diarios de la Finca del Fuego.\n\n—Así es... —respondió Kokushibo, poniéndose de pie con una elegancia aterradora—. Para superar a mi hermano y escapar de la maldición de la muerte a los veinticinco años, vendí mi alma a Muzan y me convertí en un demonio. Mi Respiración de la Luna es la forma perfecta e inmortal que tu respiración defectuosa jamás podrá alcanzar.\n\nKokushibo desenvainó su katana orgánica. En un milisegundo, la catacumba entera fue cortada por decenas de hojas de media luna hechas de luz plateada.",
                "img": "escena_c2_e3.jpg"
            }
        ]
    },
    {
        "titulo": "Capítulo 3: La Luna contra el Sol",
        "escenas": [
            {
                "sub": "Escena 1: La Respiración de la Luna",
                "text": "Kaito se lanzó al ataque sin dudarlo, ejecutando su Estilo del Trueno Inverso para desviar los primeros cortes de media luna. Sin embargo, la velocidad de Kokushibo pertenecía a un nivel completamente distinto.\n\n—Respiración de la Luna... Primera Postura: Luna Oscura - Palacio Nocturno.\n\nUn solo tajo de la katana de seis ojos creó docenas de cuchillas de luna flotantes que destruyeron el hombro derecho de Kaito y atravesaron la pared de piedra detrás de él.\n\nKaito cayó herido en la piedra, pero no soltó su arma.\n\n—¡Ren! ¡No intentes bloquear sus ataques! —gritó Kaito escupiendo sangre—. ¡Su espada cambia de tamaño y forma en cada golpe! ¡Tienes que ver a través del 'Mundo Transparente'!",
                "img": "escena_c3_e1.jpg"
            },
            {
                "sub": "Escena 2: El Mundo Transparente",
                "text": "Apremiado por el peligro mortal de su mentor, Ren inhaló aire hasta hacer crujir los alvéolos de sus pulmones.\n\nSu corazón latió a más de doscientos diez pulsaciones por minuto. La marca en su cara se expandió por todo el cuello hasta el pecho. De pronto, la visión de Ren cambió por completo: el aire a su alrededor se volvió transparente, permitiéndole ver los músculos, los vasos sanguíneos y el flujo de aire dentro del cuerpo de Kokushibo.\n\nRen podía ver la intención del ataque del Primer Lunar una fracción de segundo antes de que la criatura moviera su espada.\n\n—Ha alcanzado el Mundo Transparente... —pensó Kokushibo con una sombra de sorpresa en sus seis ojos.\n\nRen esquivó la estocada de la Luna por milímetros y lanzó un tajo vertical de llamas doradas.",
                "img": "escena_c3_e2.jpg"
            },
            {
                "sub": "Escena 3: La Piedra del Primer Herrero",
                "text": "La hoja negra de Ren chocó contra la katana de carne de Kokushibo, levantando un estallido de chispas rojas y púrpuras que iluminó la catacumba.\n\nEl chico del haori amarillo, actuando por puro instinto en su estado de trance, atacó el flanco izquierdo con un destello de electricidad que cortó dos de los ojos de Kokushibo.\n\nAcorralado por la combinación del Mundo Transparente y la velocidad del trueno, Kokushibo dio un paso hacia atrás. Su mirada se fijó en la losa de piedra del altar tras el choque: allí descansaba la Piedra de Afilado Solar, la herramienta sagrada que Ren buscaba.\n\n—Esta pequeña victoria no cambiará el destino... —dijo Kokushibo, retrocediendo hacia las sombras de las catacumbas—. Nos veremos en el palacio... cuando la sangre de la chica del sol sea nuestra.\n\nEl Primer Lunar desapareció en una brecha espacial, dejando la catacumba en un silencio pesado.",
                "img": "escena_c3_e3.jpg"
            }
        ]
    },
    {
        "titulo": "Capítulo 4: El Afilado de la Hoja Definitiva",
        "escenas": [
            {
                "sub": "Escena 1: El Filo de la Era Sengoku",
                "text": "Ren se acercó al altar de piedra y tomó la Piedra de Afilado Solar. La herramienta no estaba hecha de piedra común: era una aleación de mineral volcánico y cenizas de glicina antigua.\n\nKaito, con la Herida de su hombro vendada por el muchacho del haori amarillo, ayudó a Ren a preparar el agua sagrada del altar.\n\nRen comenzó el proceso de afilado de su katana negra sobre la piedra. Con cada pasada de la hoja sobre la superficie, el metal no perdía material: la línea carmesí del filo absorbía el mineral volcánico, volviéndose de un color rojo rubí tan brillante que parecía fuego líquido sobre el acero.\n\n—Esta espada ya no es una simple arma —dijo Kaito mirando el reflejo del metal—. Es el testamento de cuatrocientos años de herreros que dieron su vida por este momento.",
                "img": "escena_c4_e1.jpg"
            },
            {
                "sub": "Escena 2: La Noticia en la Superficie",
                "text": "Al salir de las catacumbas de la capital y regresar a la superficie, un grupo de cuervos mensajeros sobrevoló el cielo nocturno en una formación desordenada y de pánico.\n\n—¡Ataque a la Sede Central! ¡Ataque a la Sede Central! —gritaban las aves con desesperación—. ¡Muzan ha localizado la fortaleza del Líder Supremo! ¡Todos los Pilares deben acudir de inmediato!\n\nRen, Kaito y el chico del haori amarillo se miraron. La guerra final no esperaría al entrenamiento; había comenzado esa misma noche.\n\nRen colocó la Katana del Sol pulida en su funda, ajustó la caja de Miyuki en su espalda y se lanzó a correr a máxima velocidad a través del bosque.",
                "img": "escena_c4_e2.jpg"
            },
            {
                "sub": "Escena 3: La Llegada del Rey",
                "text": "En la Sede Central del Gremio Cuervo, las barreras de flores de glicina habían sido reducidas a cenizas por el fuego de sangre de las tropas de Muzan.\n\nEl Líder Supremo del Gremio permanecía sentado en su veránda de madera, esperando pacientemente. Frente a él, caminando sobre el pasto ensangrentado del jardín, se encontraba Muzan en su forma de aristócrata elegante.\n\n—Al fin nos conocemos... Ubuyashiki —dijo Muzan con una sonrisa helada—. Tu estirpe de cazadores termina esta noche.\n\n—Te equivocas, Muzan —respondió el Líder Supremo sonriendo con amabilidad—. La voluntad humana no muere cuando el líder cae. Se transmite de generación en generación como una llama que jamás podrás apagar.",
                "img": "escena_c4_e3.jpg"
            }
        ]
    },
    {
        "titulo": "Capítulo 5: La Gran Explosión (Clímax del Volumen 6)",
        "escenas": [
            {
                "sub": "Escena 1: El Sacrificio del Líder",
                "text": "Muzan dio un paso hacia la veránda para decapitar al Líder Supremo con sus garras.\n\nPero antes de que las garras tocaran el cuello del hombre, el Líder Supremo detonó los cientos de barriles de pólvora y sustancias inflamables que había ocultado bajo los cimientos de madera de su propia casa.\n\nUna explosión gigantesca de fuego y esquirlas de hierro sagrado destruyó la Sede Central por completo, iluminando el cielo de la noche como si fuera pleno mediodía.\n\nEl cuerpo de Muzan fue destrozado en mil pedazos por la fuerza de la explosión y las esquirlas de metal impregnadas con veneno de glicina concentrado.\n\nLos Pilares, que llegaban a la zona en ese milisegundo, presenciaron el sacrificio de su líder con una mezcla de dolor e ira incontrolable.",
                "img": "escena_c5_e1.jpg"
            },
            {
                "sub": "Escena 2: La Regeneración del Monstruo",
                "text": "A pesar del veneno y la fuerza de la explosión, las masas de carne de Muzan comenzaron a juntarse en el centro del cráter a una velocidad aterradora. Su cuerpo se regeneró en menos de diez segundos, adoptando una forma de combate monstruosa con bocas y tentáculos de hueso emergiendo de sus brazos.\n\n—¡Inútil! ¡Inútil! —gritó Muzan con rabia—. ¡Un truco sucio de un humano moribundo no puede matarme!\n\nGyomei, el Pilar de la Piedra, fue el primero en saltar al cráter. Con un movimiento devastador de su hacha de hierro y bola de picos unidas por una cadena, destruyó la cabeza de Muzan en pleno proceso de regeneración.\n\n—¡No dejen que se recupere! —gritó Gyomei—. ¡Ataquen todos a la vez!",
                "img": "escena_c5_e2.jpg"
            },
            {
                "sub": "Escena 3: La Caída al Castillo Infinito (Cierre del Tomo 6)",
                "text": "Todos los Pilares —incluyendo a Ren, Kanae, Muichiro y Mitsuri— se arrojaron sobre Muzan con sus katanas cargadas con sus respectivas respiraciones.\n\nPero antes de que los filos de las espadas tocaran el cuerpo del Rey Oni, el sonido seco de una cuerda de biwa (¡TONG!) resonó bajo el suelo del cráter.\n\nLa tierra bajo los pies de los cazadores se abrió por completo.\n\nCientos de puertas de madera de estilo tradicional emergieron del abismo. Todos los cazadores del gremio, junto a Ren y Miyuki, cayeron al vacío, siendo absorbidos hacia las diferentes estructuras flotantes del Castillo Infinito.\n\nMuzan sonrió con malicia mientras caía rodeado por los demonios supervivientes.\n\n—Bienvenidos a mi dominio... cazadores —resonó la voz de Muzan mientras las puertas se cerraban sobre el cielo de la noche—. Aquí es donde sus almas serán devoradas.\n\n\n                  [ CONTINUARÁ EN EL VOLUMEN 7 ]\n                  [ INICIO DEL ARCO DEL CASTILLO INFINITO ]",
                "img": "escena_c5_e3.jpg"
            }
        ]
    }
]

for cap in capitulos:
    p_c = doc.add_paragraph()
    run_c = p_c.add_run(cap["titulo"])
    run_c.font.name = "Arial"
    run_c.font.size = Pt(18)
    run_c.font.bold = True
    run_c.font.color.rgb = RGBColor(160, 0, 0)
    
    for esc in cap["escenas"]:
        p_sub = doc.add_paragraph()
        run_sub = p_sub.add_run(esc["sub"])
        run_sub.font.name = "Arial"
        run_sub.font.size = Pt(14)
        run_sub.font.bold = True
        run_sub.font.color.rgb = RGBColor(50, 50, 50)
        
        p_t = doc.add_paragraph()
        run_t = p_t.add_run(esc["text"])
        run_t.font.name = "Calibri"
        run_t.font.size = Pt(12)
        
        img_path = base_dir / esc["img"]
        if img_path.exists():
            doc.add_picture(str(img_path), width=Inches(5.5))
            doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER
        doc.add_paragraph()
        
    doc.add_page_break()

docx_out1 = base_dir / "libro.docx"
docx_out2 = dest2 / "libro.docx"

doc.save(str(docx_out1))
doc.save(str(docx_out2))
print(f"Generated libro.docx for Vol 6 successfully at {docx_out1}")
