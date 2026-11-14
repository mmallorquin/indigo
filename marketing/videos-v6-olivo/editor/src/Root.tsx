import { Composition, Folder } from "remotion";
import { Video01, Video02, Video03, Video04 } from "./CollectionA";
import { Video05, Video06, Video07 } from "./CollectionB";
import { Video08, Video09, Video10 } from "./CollectionC";
import { Type, End } from "./Brand";
export const RemotionRoot = () => (
  <>
    <Folder name="Coleccion-Olivo">
      <Composition
        id="01-Consulta"
        component={Video01}
        width={1080}
        height={1920}
        fps={30}
        durationInFrames={570}
      />
      <Composition
        id="02-Chalecos"
        component={Video02}
        width={1080}
        height={1920}
        fps={30}
        durationInFrames={540}
      />
      <Composition
        id="03-Basicas"
        component={Video03}
        width={1080}
        height={1920}
        fps={30}
        durationInFrames={540}
      />
      <Composition
        id="04-Mangas-Largas"
        component={Video04}
        width={1080}
        height={1920}
        fps={30}
        durationInFrames={540}
      />
      <Composition
        id="05-Sastrero"
        component={Video05}
        width={1080}
        height={1920}
        fps={30}
        durationInFrames={540}
      />
      <Composition
        id="06-Blusa"
        component={Video06}
        width={1080}
        height={1920}
        fps={30}
        durationInFrames={540}
      />
      <Composition
        id="07-Conjuntos"
        component={Video07}
        width={1080}
        height={1920}
        fps={30}
        durationInFrames={600}
      />
      <Composition
        id="08-Cuellos"
        component={Video08}
        width={1080}
        height={1920}
        fps={30}
        durationInFrames={540}
      />
      <Composition
        id="09-Azul-Crema"
        component={Video09}
        width={1080}
        height={1920}
        fps={30}
        durationInFrames={540}
      />
      <Composition
        id="10-Jeans"
        component={Video10}
        width={1080}
        height={1920}
        fps={30}
        durationInFrames={600}
      />
    </Folder>
    <Folder name="Elementos">
      <Composition
        id="Tipografia"
        component={Type}
        width={1080}
        height={1920}
        fps={30}
        durationInFrames={90}
        defaultProps={{
          text: "Índigo\na tu manera",
          size: 100,
          color: "#4F5533",
          x: 86,
          y: 400,
        }}
      />
      <Composition
        id="Cierre"
        component={End}
        width={1080}
        height={1920}
        fps={30}
        durationInFrames={120}
        defaultProps={{
          cta: "Consultá por",
          keyword: "tu próximo look",
          number: "01",
        }}
      />
    </Folder>
  </>
);
