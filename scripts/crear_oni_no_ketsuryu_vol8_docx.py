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
run_title = p_title.add_run("Oni no Ketsuryū (鬼の血流 - La Estirpe de la Sangre)\nVolumen 8: El Juicio de los Tres Lunares Superiores")
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

base_dir = Path(r"C:\Proyectos\mis-libros-editorial\libros\oni-no-ketsuryu-volumen-8")
dest2 = Path(r"c:\Users\nicol\Downloads\MIS LIBROS\libros\oni-no-ketsuryu-volumen-8")

base_dir.mkdir(parents=True, exist_ok=True)
dest2.mkdir(parents=True, exist_ok=True)

# Asignar imagenes base si falta alguna
ref_dir = Path(r"C:\Proyectos\mis-libros-editorial\libros\oni-no-ketsuryu-volumen-7")

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
        "titulo": "Capítulo 1: El Espejo de las Sombras",
        "escenas": [
            {
                "sub": "Escena 1: El Salón de la Luna Creciente",
                "text": "Tras la caída del Castillo Infinito hacia las capas subterráneas de la capital, el espacio se dividió en sectores aislados por biwas mágicos.\n\nRen y Kaito (el cazador de la máscara de Tengu) cayeron en una catedral subterránea hecha de piedra negra y espejos flotantes. En el centro del altar, esperándolos con una calma aterradora, se encontraba Akaza, el Tercer Lunar Rojo, el mismo demonio que había asesinado al Pilar del Fuego (Kenshin) en el Tren de las Sombras.\n\nAkaza los miró con sus ojos dorados marcados, ajustando sus puños llenos de tatuajes azules.\n\n—Has crecido, chico de la marca... —dijo Akaza con una sonrisa desafiante—. Siento el calor del fuego de Kenshin en tu espada. Demuéstrame si eres digno de llevar su herencia.",
                "img": "escena_c1_e1.jpg"
            },
            {
                "sub": "Escena 2: La Brújula de Agujas",
                "text": "Sin decir una palabra, Akaza desató su Arte Demoníaco: Brújula de Agujas. Una brújula de luz azul con forma de copo de nieve se desplegó bajo sus pies, permitiéndole detectar el 'espíritu de combate' y la intención de ataque de Ren antes de que este pudiera mover un solo músculo.\n\nCada estocada de la katana negra de Ren fue desviada por los puños de energía de Akaza a milímetros del impacto.\n\n—¡Es inútil! —gritó Akaza, lanzando una ráfaga de golpes que agrietó la piedra del altar—. ¡Mientras tengas espíritu de combate, mi brújula predecirá todos tus movimientos!\n\nKaito saltó desde el aire, desenvainando su katana carmesí para cubrir la guardia de Ren, pero la fuerza bruta de Akaza rompió dos de las costillas de Kaito de un solo impacto.",
                "img": "escena_c1_e2.jpg"
            },
            {
                "sub": "Escena 3: El Silencio del Alma",
                "text": "Acorralado contra las columnas de piedra, Ren recordó las palabras que el Pilar de la Piedra le dijo durante el entrenamiento:\n\n«Para cortar a quien lee tu intención, debes vaciar tu mente... Apaga el deseo de matar y vuélvete tan transparente como el aire.»\n\nRen cerró los ojos por tres segundos en medio de la ráfaga de golpes. Inhaló suavemente, apagando toda su ira y su deseo de venganza.\n\nDe pronto, en la visión de Akaza, la presencia de Ren desapareció por completo de la brújula, a pesar de que el joven seguía parado a dos metros de él.\n\nRen había alcanzado el Estado de Anulación de Intención.",
                "img": "escena_c1_e3.jpg"
            }
        ]
    },
    {
        "titulo": "Capítulo 2: La Redención del Guerrero",
        "escenas": [
            {
                "sub": "Escena 1: El Corte Invariable",
                "text": "Sin emitir un solo espíritu de combate, Ren se desplazó como una sombra invisible para la brújula de Akaza.\n\n—Danza del Sol... Quinta Postura: Espejo del Sol Feroz.\n\nLa katana roja de Ren trazó un arco silencioso de fuego dorado que atravesó la guardia de Akaza. La hoja cortó el cuello del Tercer Lunar de un solo tajo limpio antes de que la criatura pudiera reaccionar.\n\nLa cabeza de Akaza salió volando, rebotando sobre las losas de la catedral.",
                "img": "escena_c2_e1.jpg"
            },
            {
                "sub": "Escena 2: Los Recuerdos del Dojo Hakuji",
                "text": "Al perder la cabeza, el cuerpo de Akaza intentó regenerarse por pura fuerza de voluntad. Sin embargo, al tocar las cenizas de su propia carne, sus recuerdos humanos reprimidos por mil años volvieron en oleadas a su mente.\n\nSe vio a sí mismo cuando era un joven humano llamado Hakuji, cuidando a su padre enfermo y enamorándose de Koyuki, la hija de su maestro de artes marciales. Recordó cómo un dojo rival envenenó el pozo de agua de su hogar, matando a su prometida y a su maestro mientras él estaba fuera.\n\nEl odio lo convirtió en demonio, pero en el fondo, Hakuji solo quería proteger a la mujer que amaba.\n\n—Ya no tengo a nadie a quien proteger... —pensó el espíritu de Hakuji, mirando a la ilusión de Koyuki que lo esperaba en la luz.",
                "img": "escena_c2_e2.jpg"
            },
            {
                "sub": "Escena 3: El Fin del Tercer Lunar",
                "text": "Aceptando su derrota y recordando la dignidad que tenía como ser humano, Akaza dirigió su propia energía demoníaca hacia su torso, destruyendo su propia regeneración desde adentro.\n\nSu cuerpo se disolvió en un polvo dorado que fue absorbido por las baldosas de la catedral.\n\nRen cayó sobre una rodilla, apoyándose en su katana quebrada, y realizó una breve inclinación de cabeza hacia las cenizas del enemigo que al fin había encontrado la paz.\n\n—Descansa en paz... Hakuji —susurró Ren.",
                "img": "escena_c2_e3.jpg"
            }
        ]
    },
    {
        "titulo": "Capítulo 3: El Veneno de la Luna Llena",
        "escenas": [
            {
                "sub": "Escena 1: El Encuentro con la Luna Superior Dos",
                "text": "En el sector oeste del castillo, entre jardines flotantes de loto de cristal, se libraba la batalla contra Doma, el Segundo Lunar Rojo.\n\nKanae (la chica de la máscara de zorro) y Inosuke (el chico del haori amarillo) luchaban desesperadamente contra las esculturas de hielo gigantescas que Doma invocaba con sus abanicos.\n\nDoma sonreía con su habitual apatía, lanzando ráfagas de escarcha a temperatura bajo cero que congelaban la sangre dentro de las heridas de los cazadores.\n\n—Son bastante persistentes... —dijo Doma, desplegando su abanico de cristal—. Pero el aire de este salón ya está lleno de mis microcristales de hielo. Sus pulmones se destruirán con cada respiración que den.",
                "img": "escena_c3_e1.jpg"
            },
            {
                "sub": "Escena 2: El Plan de la Mariposa",
                "text": "Kanae sabiendo que no podía superar la fuerza de Doma en un combate frontal, puso en marcha el plan que había preparado con la médica del gremio.\n\nAvanzó en una arremetida suicida, permitiendo que Doma la atrapara con sus garras heladas y la absorbiera dentro de su cuerpo.\n\n—¡KANAE! —gritó Inosuke, lanzándose hacia adelante con el trueno envolviendo sus espaldas.\n\nPero Doma no sabía que Kanae había consumido durante un año entero dosis masivas de veneno de glicina concentrado. Cincuenta kilos de toxina pura entraron al torrente sanguíneo del demonio al mismo tiempo.",
                "img": "escena_c3_e2.jpg"
            },
            {
                "sub": "Escena 3: La Licuefacción del Demonio",
                "text": "Cinco minutos después, el efecto de la toxina de glicina destruyó la estructura celular de Doma desde adentro. Sus órganos se convirtieron en líquido y la piel de su rostro comenzó a caerse a pedazos sobre la nieve.\n\n—¿Qué es esto...? Mi regeneración... no funciona... —gimió Doma, perdiendo el equilibrio.\n\nInosuke, aprovechando la parálisis del enemigo, ejecutó su Respiración del Trueno: Séptima Postura, cruzando el cuello de Doma a la velocidad de la luz.\n\nLa cabeza del Segundo Lunar Rojo fue amputada definitivamente, disolviéndose en una masa de veneno morado y cenizas.",
                "img": "escena_c3_e3.jpg"
            }
        ]
    },
    {
        "titulo": "Capítulo 4: Las Seis Ojos del Abismo",
        "escenas": [
            {
                "sub": "Escena 1: El Salón de las Mil Espadas",
                "text": "En el centro más profundo del castillo, el grupo principal —compuesto por Gyomei (Pilar de la Piedra), Sanemi (Pilar del Viento), Muichiro (Pilar de la Niebla) y Ren— llegó a la cámara más imponente de la fortaleza.\n\nAllí los esperaba Kokushibo, el Primer Lunar Rojo, el guerrero de seis ojos que vestía un kimono púrpura y sostenía la katana de carne viviente cubierta de pupilas.\n\nSu sola presencia emitía una gravedad física que agrietó el suelo de piedra.\n\n—Cuatro cazadores marcados... —habló Kokushibo con su voz profunda—. Una cosecha digna para probar el filo de la Respiración de la Luna.",
                "img": "escena_c4_e1.jpg"
            },
            {
                "sub": "Escena 2: La Tormenta de las Cuchillas Lunares",
                "text": "Kokushibo desenvainó su espada. Con un solo movimiento, desató una tormenta de cientos de cuchillas de luz plateada en forma de media luna que rebotaron por las paredes y el techo de la habitación.\n\nGyomei usó su bola de picos y hacha unidas por cadena para desviar el ataque principal, mientras Sanemi bloqueaba con ráfagas de viento.\n\nA pesar de la defensa perfecta de los Pilares, las cuchillas de luna cambiaban de tamaño y dirección de forma impredecible, infligiendo cortes profundos en los brazos y piernas de los cuatro luchadores.\n\n—Su espada no tiene una longitud fija... —advirtió Muichiro, activando la marca de la niebla en su cara—. ¡Puede extender la hoja a través del espacio!",
                "img": "escena_c4_e2.jpg"
            },
            {
                "sub": "Escena 3: La Visión del Mundo Transparente",
                "text": "Ren inhaló hasta el límite de sus pulmones, haciendo latir su corazón a más de doscientas pulsaciones por minuto.\n\nSu visión cambió: el entorno se volvió transparente y pudo ver la estructura ósea, los puntos de flujo de sangre y la intención muscular de Kokushibo. Al mismo tiempo, las katanas de Gyomei, Sanemi y Ren se tiñeron de un color rojo rubí incandescente por el calor de sus agarres marcados.\n\nLas espadas rojas ralentizaban la regeneración del Primer Lunar a nivel celular.\n\n—Han empuñado las 'Hojas Rojas'... —pensó Kokushibo, poniéndose en guardia seria por primera vez en cuatrocientos años.",
                "img": "escena_c4_e3.jpg"
            }
        ]
    },
    {
        "titulo": "Capítulo 5: La Caída del Primer Samurai (Clímax del Volumen 8)",
        "escenas": [
            {
                "sub": "Escena 1: El Empalamiento de la Niebla",
                "text": "Muichiro (el Pilar de la Niebla de catorce años) se lanzó en un ataque suicida.\n\nDejó que la katana de carne de Kokushibo le atravesara el torso, usando su propio cuerpo como freno físico para clavar su hoja roja directamente en el costado del Primer Lunar. El calor del metal rojo paralizó los nervios del demonio por tres segundos cruciales.\n\n—¡AHORA! ¡NO DUDEN! —gritó Muichiro con sangre en los labios.\n\nSanemi y Gyomei descargaron todo el peso de sus armas sobre el cuello de Kokushibo con un impacto destructivo.",
                "img": "escena_c5_e1.jpg"
            },
            {
                "sub": "Escena 2: La Decapitamiento Doble",
                "text": "Ren aprovechó la brecha abierta por Muichiro. Ejecutó la postura más rápida de la Danza del Sol:\n\n—Danza del Sol... Decimoprimera Postura: Halo del Sol Abrillantado.\n\nLa katana roja de Ren se unió al hacha de Gyomei, cortando simultáneamente la garganta de Kokushibo. La cabeza del Primer Lunar Rojo, con sus seis ojos abiertos en estado de shock, fue amputada del cuerpo, volando en medio de un estallido de chispas rojas y doradas.\n\nEl cuerpo de Muichiro cayó a un lado, habiendo entregado su vida para garantizar el golpe.",
                "img": "escena_c5_e2.jpg"
            },
            {
                "sub": "Escena 3: El Espejo de la Monstruosidad (Cierre del Tomo 8)",
                "text": "Aunque la cabeza de Kokushibo cayó al suelo, el cuerpo intentó regenerar un rostro nuevo y deforme con cuernos de pesadilla para seguir luchando.\n\nSin embargo, al mirar su reflejo en el metal pulido de la espada rota de Muichiro que yacía en el suelo, Kokushibo vio en lo que se había convertido: un monstruo horrendo que había vendido su honor de samurai por miedo a la muerte.\n\n—¿Es esto... lo que quería ser...? —pensó Kokushibo con un arrepentimiento infinito.\n\nSu propia culpa detuvo la regeneración. Su cuerpo se disolvió por completo en cenizas negras, dejando únicamente su antigua flauta de madera sobre las losas.\n\nEn ese instante, la estructura del Castillo Infinito comenzó a temblar con violencia: la fortaleza completa estaba siendo forzada a subir a la superficie por la caída de los Lunares.\n\n\n                  [ CONTINUARÁ EN EL VOLUMEN 9 ]\n                  [ INICIO DE LA BATALLA EN LA SUPERFICIE ]",
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
print(f"Generated libro.docx for Vol 8 successfully at {docx_out1}")
