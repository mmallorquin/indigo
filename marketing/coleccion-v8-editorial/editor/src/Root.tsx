import {
  Composition,
  Still,
  Folder,
  Sequence,
  useVideoConfig,
  interpolate,
  staticFile,
} from "remotion";
import { Audio } from "@remotion/media";
import { Artwork, type Layout } from "./Artwork";
import data from "./contenido.json";
const Scene = ({ index, film }: { index: number; film: number }) => (
  <Artwork layout={data.reels[film].scenes[index] as Layout} animate />
);
const NeutroInicio = () => <Scene index={0} film={0} />;
const NeutroPrenda = () => <Scene index={1} film={0} />;
const NeutroLook = () => <Scene index={2} film={0} />;
const NeutroContraste = () => <Scene index={3} film={0} />;
const NeutroCierre = () => <Scene index={4} film={0} />;
const PantalonInicio = () => <Scene index={0} film={1} />;
const PantalonCintura = () => <Scene index={1} film={1} />;
const PantalonJean = () => <Scene index={2} film={1} />;
const PantalonMedidas = () => <Scene index={3} film={1} />;
const PantalonCierre = () => <Scene index={4} film={1} />;
const Music = ({ src }: { src: string }) => {
  const { fps, durationInFrames } = useVideoConfig();
  return (
    <Audio
      src={staticFile("audio/" + src)}
      volume={(f) =>
        interpolate(
          f,
          [0, 0.7 * fps, durationInFrames - 1.2 * fps, durationInFrames],
          [0, 0.82, 0.82, 0],
          { extrapolateLeft: "clamp", extrapolateRight: "clamp" },
        )
      }
      premountFor={fps}
    />
  );
};
const Neutros = () => {
  const { fps } = useVideoConfig();
  return (
    <>
      <Music src="03.wav" />
      <Sequence
        name="Apertura editorial"
        from={0}
        durationInFrames={3 * fps}
        premountFor={fps}
      >
        <NeutroInicio />
      </Sequence>
      <Sequence
        name="Sastrero — prenda completa"
        from={3 * fps}
        durationInFrames={4.5 * fps}
        premountFor={fps}
      >
        <NeutroPrenda />
      </Sequence>
      <Sequence
        name="Marrón — look completo"
        from={7.5 * fps}
        durationInFrames={4.5 * fps}
        premountFor={fps}
      >
        <NeutroLook />
      </Sequence>
      <Sequence
        name="Beige y negro — contraste"
        from={12 * fps}
        durationInFrames={4.5 * fps}
        premountFor={fps}
      >
        <NeutroContraste />
      </Sequence>
      <Sequence
        name="Consulta"
        from={16.5 * fps}
        durationInFrames={5.5 * fps}
        premountFor={fps}
      >
        <NeutroCierre />
      </Sequence>
    </>
  );
};
const Pantalones = () => {
  const { fps } = useVideoConfig();
  return (
    <>
      <Music src="07.wav" />
      <Sequence
        name="Apertura — díptico"
        from={0}
        durationInFrames={3 * fps}
        premountFor={fps}
      >
        <PantalonInicio />
      </Sequence>
      <Sequence
        name="Sastrero — cintura"
        from={3 * fps}
        durationInFrames={4.5 * fps}
        premountFor={fps}
      >
        <PantalonCintura />
      </Sequence>
      <Sequence
        name="Jean — bolsillo y lavado"
        from={7.5 * fps}
        durationInFrames={4.5 * fps}
        premountFor={fps}
      >
        <PantalonJean />
      </Sequence>
      <Sequence
        name="Guía de medidas"
        from={12 * fps}
        durationInFrames={5 * fps}
        premountFor={fps}
      >
        <PantalonMedidas />
      </Sequence>
      <Sequence
        name="Consulta"
        from={17 * fps}
        durationInFrames={5 * fps}
        premountFor={fps}
      >
        <PantalonCierre />
      </Sequence>
    </>
  );
};
const Post = ({ index }: { index: number }) => (
  <Artwork layout={data.posts[index] as Layout} />
);
export const RemotionRoot = () => (
  <>
    <Composition
      id="14-Neutros"
      component={Neutros}
      durationInFrames={660}
      fps={30}
      width={1080}
      height={1920}
    />
    <Composition
      id="15-Pantalones"
      component={Pantalones}
      durationInFrames={660}
      fps={30}
      width={1080}
      height={1920}
    />
    <Folder name="Carrusel-Neutros">
      <Still
        id="Neutros-01"
        component={Post}
        defaultProps={{ index: 0 }}
        width={1080}
        height={1350}
      />
      <Still
        id="Neutros-02"
        component={Post}
        defaultProps={{ index: 1 }}
        width={1080}
        height={1350}
      />
      <Still
        id="Neutros-03"
        component={Post}
        defaultProps={{ index: 2 }}
        width={1080}
        height={1350}
      />
      <Still
        id="Neutros-04"
        component={Post}
        defaultProps={{ index: 3 }}
        width={1080}
        height={1350}
      />
      <Still
        id="Neutros-05"
        component={Post}
        defaultProps={{ index: 4 }}
        width={1080}
        height={1350}
      />
    </Folder>
    <Folder name="Carrusel-Pantalones">
      <Still
        id="Pantalones-01"
        component={Post}
        defaultProps={{ index: 5 }}
        width={1080}
        height={1350}
      />
      <Still
        id="Pantalones-02"
        component={Post}
        defaultProps={{ index: 6 }}
        width={1080}
        height={1350}
      />
      <Still
        id="Pantalones-03"
        component={Post}
        defaultProps={{ index: 7 }}
        width={1080}
        height={1350}
      />
      <Still
        id="Pantalones-04"
        component={Post}
        defaultProps={{ index: 8 }}
        width={1080}
        height={1350}
      />
      <Still
        id="Pantalones-05"
        component={Post}
        defaultProps={{ index: 9 }}
        width={1080}
        height={1350}
      />
    </Folder>
    <Folder name="Escenas-editables">
      <Composition
        id="Neutro-Inicio"
        component={NeutroInicio}
        durationInFrames={90}
        fps={30}
        width={1080}
        height={1920}
      />
      <Composition
        id="Neutro-Prenda"
        component={NeutroPrenda}
        durationInFrames={135}
        fps={30}
        width={1080}
        height={1920}
      />
      <Composition
        id="Neutro-Look"
        component={NeutroLook}
        durationInFrames={135}
        fps={30}
        width={1080}
        height={1920}
      />
      <Composition
        id="Neutro-Contraste"
        component={NeutroContraste}
        durationInFrames={135}
        fps={30}
        width={1080}
        height={1920}
      />
      <Composition
        id="Neutro-Cierre"
        component={NeutroCierre}
        durationInFrames={165}
        fps={30}
        width={1080}
        height={1920}
      />
      <Composition
        id="Pantalon-Inicio"
        component={PantalonInicio}
        durationInFrames={90}
        fps={30}
        width={1080}
        height={1920}
      />
      <Composition
        id="Pantalon-Cintura"
        component={PantalonCintura}
        durationInFrames={135}
        fps={30}
        width={1080}
        height={1920}
      />
      <Composition
        id="Pantalon-Jean"
        component={PantalonJean}
        durationInFrames={135}
        fps={30}
        width={1080}
        height={1920}
      />
      <Composition
        id="Pantalon-Medidas"
        component={PantalonMedidas}
        durationInFrames={150}
        fps={30}
        width={1080}
        height={1920}
      />
      <Composition
        id="Pantalon-Cierre"
        component={PantalonCierre}
        durationInFrames={150}
        fps={30}
        width={1080}
        height={1920}
      />
    </Folder>
  </>
);
